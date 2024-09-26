"""
Contains validation logic for TripicaCustomerLoaderDataSet
"""

import re
from datetime import date, datetime
from typing import Any, Generator, Optional, TypeAlias, TypeVar

from bomf.config import MigrationConfig
from dateutil.relativedelta import relativedelta
from email_validator import validate_email
from ibims.bo4e import Adresse, Anrede, Landescode, VertragskontoCBA, VertragskontoMBA, ZusatzAttribut
from ibims.datasets import TripicaCustomerLoaderDataSet
from injector import Module, provider
from more_itertools import first_true
from pvframework import (
    ParallelQueryMappedValidator,
    PathMappedValidator,
    Query,
    QueryMappedValidator,
    ValidationManager,
    Validator,
)
from pvframework.errors import ValidationMode
from pvframework.types import SyncValidatorFunction
from pvframework.utils import param, required_field
from pytz import timezone
from schwifty import BIC, IBAN

from .utils import migration_config
from .validation_manager import ValidationManagerWithConfig

_berlin = timezone("Europe/Berlin")


def get_zusatz_attribut(name: str, zusatz_attribute: list[ZusatzAttribut]) -> Optional[str]:
    """
    Extracts a value from a list of `ZusatzAttribut`. Returns None if there doesn't exist an `ZusatzAttribut` of
    name `name`.
    """
    zusatz_attribut = first_true(zusatz_attribute, default=None, pred=lambda zus_ref: zus_ref.name == name)
    return zusatz_attribut.wert if zusatz_attribut is not None else None


def check_geschaeftspartner_anrede(anrede: Anrede):
    """
    geschaeftspartner.anrede must be one of the following: HERR, FRAU, FIRMA, EHELEUTE
    """
    valid_values_strings = {Anrede.HERR, Anrede.FRAU, Anrede.FIRMA, Anrede.EHELEUTE}
    if anrede not in valid_values_strings:
        raise ValueError(
            f"{param('anrede').param_id} must be one of the following: " f"{', '.join(valid_values_strings)}"
        )


def check_str_is_stripped(string: str):
    """
    geschaeftspartner.nachname must not start with whitespace. Further validation is difficult because e.g.
    there exist names with characters like '.
    And if the name is a company it could even contain digits or other characters e.g. 'edi@energy'.
    """
    if string.strip() != string:
        raise ValueError(f"{param('string').param_id} must not start or end with whitespace.")


def check_e_mail(e_mail: Optional[str] = None):
    """
    geschaeftspartner.e_mail_adresse must match the regex pattern `REGEX_E_MAIL`.
    """
    if not e_mail:
        return
    validate_email(e_mail, check_deliverability=False)


def check_extern_customer_id(zusatz_attribute: list[ZusatzAttribut]):
    """
    geschaeftspartner.zusatz_attribute -> customerID has to start with 2 followed by 8 digits.
    """
    customer_id = get_zusatz_attribut("customerID", zusatz_attribute)
    if customer_id is None:
        raise ValueError("No Zusatzattribute with name customerID")
    if re.match(r"^2\d{8}$", customer_id) is None:
        raise ValueError(
            f"{param('zusatz_attribute').param_id} -> customerID has to start with 2 followed by 8 digits."
        )


def check_date_in_past_required(past_date: datetime):
    """
    The date is required and must be in the past as of the migration_key_date
    """
    config = migration_config()
    if past_date.astimezone(_berlin).date() > config.migration_key_date.astimezone(_berlin).date():
        raise ValueError(
            f"{param('past_date').param_id} must be in the past as of " + str(config.migration_key_date.isoformat())
        )


def check_date_in_future_required(future_date: datetime):
    """
    The date is required and must be in the future as of the migration_key_date
    """
    config = migration_config()
    if future_date < config.migration_key_date:
        raise ValueError(
            f"{param('future_date').param_id} must be in the future as of " + str(config.migration_key_date.isoformat())
        )


def check_date_in_past_optional(past_date: Optional[datetime] = None):
    """
    The date is optional and must be in the past as of the migration_key_date
    """
    config = migration_config()
    if (
        past_date is not None
        and past_date.astimezone(_berlin).date() > config.migration_key_date.astimezone(_berlin).date()
    ):
        raise ValueError(
            f"{param('past_date').param_id} must be in the past as of " + str(config.migration_key_date.isoformat())
        )


def check_date_in_future_optional(future_date: Optional[datetime] = None):
    """
    The date is optional and must be in the future as of the migration_key_date
    """
    config = migration_config()
    if future_date is not None and future_date < config.migration_key_date:
        raise ValueError(
            f"{param('future_date').param_id} must be in the future as of " + str(config.migration_key_date.isoformat())
        )


def check_date_in_past_bankverbindung(is_sepa_zahler: bool, past_date: Optional[datetime] = None):
    """
    The date is required if customer is sepa_zahler, and must be in the past as of the migration_key_date
    """
    config = migration_config()
    if is_sepa_zahler:
        if past_date is None:
            raise ValueError(f"{param('past_date').param_id} is required for sepa_zahler")
        if past_date.astimezone(_berlin).date() > config.migration_key_date.astimezone(_berlin).date():
            raise ValueError(
                f"{param('past_date').param_id} must be in the past as of " + str(config.migration_key_date.isoformat())
            )


def check_geschaeftspartner_geburtsdatum(geburtsdatum: datetime):
    """
    geschaeftspartner.geburtsdatum must be at least 18 years ago in the past but not earlier than 1900-01-01.
    """
    config = migration_config()
    birthday_date = geburtsdatum.astimezone(_berlin).date()
    latest_18 = config.migration_key_date.astimezone(_berlin).date() - relativedelta(years=18)
    earliest_birthday = date(1900, 1, 1)
    if birthday_date > latest_18 or birthday_date < earliest_birthday:
        # Had to use dateutil here, because I didn't want to manually catch the case if somebody was born on 29th
        # stdlib timedelta doesn't support years as kwarg
        # February.
        raise ValueError(
            f"{param('geburtsdatum').param_id} must be in the range of " f"{earliest_birthday} to {latest_18}."
        )


REGEX_TEL_NR = re.compile(r"^(\+?[1-9]|0)[0-9]{7,14}$")


def check_telefonnummer(telefonnummer: Optional[str] = None):
    r"""
    telefonnummer must match the regex pattern `REGEX_TEL_NR` (ignoring all following characters: r"[-.\s()]").
    """
    if telefonnummer and re.match(REGEX_TEL_NR, re.sub(r"[-.\s()]", "", telefonnummer)) is None:
        raise ValueError(f"{param('telefonnummer').param_id} does not match the regex pattern " "for phone numbers.")


def check_address_deutsch(address: Adresse):
    """
    address must be in germany.
    """
    if required_field(address, "landescode", Landescode) != Landescode.DE:  # type:ignore[attr-defined]
        raise ValueError(f"{param('address').param_id}.landescode must be 'DE'")
    if not re.match(r"^\d{5}$", required_field(address, "postleitzahl", str)):
        raise ValueError(f"{param('address').param_id}.postleitzahl must consist of 5 digits")


def check_address_fields(address: Adresse):
    """
    This function reuses the pydantic validator function `strasse_xor_postfach` of the bo4e model `Addresse`.
    We use it here again to prevent any unwanted errors which can occur when bypassing the validator with `construct`.

    An address is valid if it contains a postfach XOR (a strasse AND hausnummer).
    This functions checks for these conditions of a valid address.

    Nur folgende Angabekombinationen sind (nach der Abfrage) möglich:
    Straße           w   f   f
    Hausnummer       w   f   f
    Postfach         f   w   f
    Postleitzahl     w   w   w
    Ort              w   w   w
    """
    param_path = param("address").param_id
    _ = (
        required_field(address, "ort", str, param_base_path=param_path),
        required_field(address, "postleitzahl", str, param_base_path=param_path),
    )
    # Taken from the old implementation of the Address validator. See
    # https://github.com/bo4e/BO4E-python/blob/4157dab6436546ba5a911b9b3767cd312ba41e97/src/bo4e/com/adresse.py#L53
    if (
        address.strasse
        and address.hausnummer
        and not address.postfach
        or not address.strasse
        and not address.hausnummer
    ):
        return
    raise ValueError('You have to define either "strasse" and "hausnummer" or "postfach".')


def check_postleitzahl(postleitzahl: str):
    """
    Check that `postleitzahl` consists of only digits and letters (case-insensitive).
    """
    if not re.match(r"^[\dA-Za-z]+$", postleitzahl):
        raise ValueError(f"{param('postleitzahl').param_id} is invalid")


def check_iban(sepa_zahler: bool, iban: Optional[str] = None):
    r"""
    If sepa_zahler is True, iban is required and it will be checked if the IBAN is valid.
    If sepa_zahler is False, the test passes.
    """
    if sepa_zahler:
        if iban is None:
            raise ValueError(f"{param('iban').param_id} is required for sepa_zahler")
        IBAN(iban).validate()


def check_bic(sepa_zahler: bool, bic: Optional[str] = None):
    """
    bic must consist of 8 or 11 alphanumeric characters.
    """
    if sepa_zahler:
        if bic is None:
            raise ValueError(f"{param('bic').param_id} is required for sepa_zahler")
        BIC(bic).validate()


def check_kontoinhaber(is_sepa_zahler: bool, kontoinhaber: Optional[str] = None):
    """
    Checks if the kontoinhaber has the syntax 'firstname lastname'. Since names are always difficult it actually only
    checks that there are no starting or ending spaces but contains at least one space in the middle of the string.
    """
    if is_sepa_zahler:
        if kontoinhaber is None:
            raise ValueError(f"{param('kontoinhaber').param_id} is required for sepa_zahler")
        if kontoinhaber.strip() == "":
            raise ValueError(f"{param('kontoinhaber').param_id} must be non-empty")


def check_bankname(is_sepa_zahler: bool, bankname: Optional[str] = None):
    """
    bankname is required for sepa_zahler and must not be empty.
    """
    if is_sepa_zahler:
        if bankname is None:
            raise ValueError(f"{param('bankname').param_id} is required for sepa_zahler")
        if not bankname.strip():
            raise ValueError(f"{param('bankname').param_id} must not be empty")


def check_vertragskontonummer(vertragskontonummer: str):
    """
    vertragskontonummer of every cba must consist of 9 digits.
    """
    if re.match(r"^\d{9}$", vertragskontonummer) is None:
        raise ValueError(f"{param('vertragskontonummer').param_id} must consist of 9 digits")


def is_datetime(date_to_check: datetime):
    """
    Check if date_to_check is of type datetime
    """
    if not isinstance(date_to_check, datetime):
        raise ValueError(f"{param('date_to_check').param_id} must be of type datetime")


ValidatorType: TypeAlias = Validator[TripicaCustomerLoaderDataSet, SyncValidatorFunction]

validate_geschaeftspartner_anrede: ValidatorType = Validator(check_geschaeftspartner_anrede)
validate_str_is_stripped: ValidatorType = Validator(check_str_is_stripped)
validate_e_mail: ValidatorType = Validator(check_e_mail)
validate_extern_customer_id: ValidatorType = Validator(check_extern_customer_id)
validate_date_in_past_required: ValidatorType = Validator(check_date_in_past_required)
validate_date_in_future_required: ValidatorType = Validator(check_date_in_future_required)
validate_date_in_past_optional: ValidatorType = Validator(check_date_in_past_optional)
validate_date_in_future_optional: ValidatorType = Validator(check_date_in_future_optional)
validate_date_in_past_bankverbindung: ValidatorType = Validator(check_date_in_past_bankverbindung)
validate_geschaeftspartner_geburtsdatum: ValidatorType = Validator(check_geschaeftspartner_geburtsdatum)
validate_telefonnummer: ValidatorType = Validator(check_telefonnummer)
validate_address_deutsch: ValidatorType = Validator(check_address_deutsch)
validate_address_fields: ValidatorType = Validator(check_address_fields)
validate_postleitzahl: ValidatorType = Validator(check_postleitzahl)
validate_iban: ValidatorType = Validator(check_iban)
validate_bic: ValidatorType = Validator(check_bic)
validate_kontoinhaber: ValidatorType = Validator(check_kontoinhaber)
validate_bankname: ValidatorType = Validator(check_bankname)
validate_vertragskontonummer: ValidatorType = Validator(check_vertragskontonummer)
validate_is_datetime: ValidatorType = Validator(is_datetime)


def iter_contract_id_dict(some_dict: dict[str, Any]) -> Generator[tuple[Any, str], None, None]:
    """
    This function is used for `Query().iter()` to iterate over a dictionary. The values of the dictionary are returned
    and the key is used for tracking for proper `ValidationError`s.
    """
    return ((value, f"[contract_id={key}]") for key, value in some_dict.items())


VertragskontoT = TypeVar("VertragskontoT", VertragskontoMBA, VertragskontoCBA)


def iter_vertragskonten(
    vertragskonten: list[VertragskontoT],
) -> Generator[tuple[VertragskontoT, str], None, None]:
    """
    This function is used for `Query().iter()` to iterate over a dictionary. The values of the dictionary are returned
    and `vertragskonto.ouid` is used for tracking for proper `ValidationError`s.
    """
    return ((vertragskonto, f"[ouid={vertragskonto.ouid}]") for vertragskonto in vertragskonten)


class ValidationManagerProviderCustomer(Module):
    """
    This module provides a ValidationManager for customer loader with an injected MigrationConfig
    """

    @provider
    def customer_validation_manager(self, config: MigrationConfig) -> ValidationManager:
        """
        This method provides a ValidationManager for customer loader with an injected MigrationConfig
        """
        customer_manager = ValidationManagerWithConfig[TripicaCustomerLoaderDataSet](
            config, manager_id="CustomerLoader"
        )
        customer_manager.register(
            PathMappedValidator(validate_geschaeftspartner_anrede, {"anrede": "geschaeftspartner.anrede"}),
            mode=ValidationMode.WARNING,
        )
        customer_manager.register(
            PathMappedValidator(validate_str_is_stripped, {"string": "geschaeftspartner.nachname"})
        )
        customer_manager.register(
            PathMappedValidator(validate_str_is_stripped, {"string": "geschaeftspartner.vorname"})
        )
        customer_manager.register(PathMappedValidator(validate_e_mail, {"e_mail": "geschaeftspartner.e_mail_adresse"}))
        customer_manager.register(
            PathMappedValidator(validate_extern_customer_id, {"zusatz_attribute": "geschaeftspartner.zusatz_attribute"})
        )
        customer_manager.register(
            PathMappedValidator(validate_date_in_past_required, {"past_date": "geschaeftspartner.erstellungsdatum"})
        )
        customer_manager.register(
            PathMappedValidator(
                validate_geschaeftspartner_geburtsdatum, {"geburtsdatum": "geschaeftspartner.geburtstag"}
            ),
            mode=ValidationMode.WARNING,
        )
        customer_manager.register(
            PathMappedValidator(validate_telefonnummer, {"telefonnummer": "geschaeftspartner.telefonnummer_privat"}),
            mode=ValidationMode.WARNING,
        )
        customer_manager.register(
            PathMappedValidator(validate_telefonnummer, {"telefonnummer": "geschaeftspartner.telefonnummer_geschaeft"}),
            mode=ValidationMode.WARNING,
        )
        customer_manager.register(
            PathMappedValidator(validate_telefonnummer, {"telefonnummer": "geschaeftspartner.telefonnummer_mobil"}),
            mode=ValidationMode.WARNING,
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_address_deutsch, {"address": Query().path("liefer_adressen").iter(iter_contract_id_dict)}
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_address_fields, {"address": Query().path("liefer_adressen").iter(iter_contract_id_dict)}
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_address_fields, {"address": Query().path("rechnungs_adressen").iter(iter_contract_id_dict)}
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_postleitzahl,
                {"postleitzahl": Query().path("rechnungs_adressen").iter(iter_contract_id_dict).path("postleitzahl")},
            )
        )
        customer_manager.register(
            ParallelQueryMappedValidator(
                validate_iban,
                {
                    "iban": Query().path("banks").iter(iter_contract_id_dict).path("iban"),
                    "sepa_zahler": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.sepa_zahler"),
                },
            )
        )
        customer_manager.register(
            ParallelQueryMappedValidator(
                validate_bic,
                {
                    "bic": Query().path("banks").iter(iter_contract_id_dict).path("bic"),
                    "sepa_zahler": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.sepa_zahler"),
                },
            )
        )
        customer_manager.register(
            ParallelQueryMappedValidator(
                validate_kontoinhaber,
                {
                    "kontoinhaber": Query().path("banks").iter(iter_contract_id_dict).path("kontoinhaber"),
                    "is_sepa_zahler": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.sepa_zahler"),
                },
            )
        )
        customer_manager.register(
            ParallelQueryMappedValidator(
                validate_date_in_past_bankverbindung,
                {
                    "past_date": Query().path("banks").iter(iter_contract_id_dict).path("gueltig_seit"),
                    "is_sepa_zahler": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.sepa_zahler"),
                },
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_date_in_future_optional,
                {"future_date": Query().path("banks").iter(iter_contract_id_dict).path("gueltig_bis")},
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_date_in_past_optional,
                {"past_date": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.gueltig_seit")},
            )
        )
        customer_manager.register(
            ParallelQueryMappedValidator(
                validate_bankname,
                {
                    "bankname": Query().path("banks").iter(iter_contract_id_dict).path("bankname"),
                    "is_sepa_zahler": Query().path("banks").iter(iter_contract_id_dict).path("sepa_info.sepa_zahler"),
                },
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_vertragskontonummer,
                {
                    "vertragskontonummer": Query()
                    .path("vertragskonten_mbas")
                    .iter(iter_vertragskonten)
                    .path("cbas")
                    .iter(iter_vertragskonten)
                    .path("vertrag.vertragsnummer")
                },
            )
        )
        customer_manager.register(
            QueryMappedValidator(
                validate_is_datetime,
                {
                    "date_to_check": Query()
                    .path("vertragskonten_mbas")
                    .iter(iter_vertragskonten)
                    .path("cbas")
                    .iter(iter_vertragskonten)
                    .path("erstellungsdatum")
                },
            )
        )
        return customer_manager
