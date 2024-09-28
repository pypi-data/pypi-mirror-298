from datetime import datetime, date, time

import validators
from validators import ValidationError as VE
from marshmallow import ValidationError
from decimal import Decimal

def validate_datetime(value: str, formats=None):
    if isinstance(value, datetime):
        return True

    # Add common formats with optional microseconds and Z for UTC
    formats = formats or [
        "%Y-%m-%d %H:%M:%S",        # Standard format
        "%Y-%m-%dT%H:%M:%S",        # ISO format without timezone
        "%Y-%m-%dT%H:%M:%S.%f",     # ISO format with microseconds
        "%Y-%m-%dT%H:%M:%S%z",      # ISO format with timezone offset
        "%Y-%m-%dT%H:%M:%S.%f%z",   # ISO format with microseconds and timezone
        "%Y-%m-%dT%H:%M:%SZ",       # ISO format with UTC (Z for zero-offset)
        "%Y-%m-%dT%H:%M:%S.%fZ",    # ISO format with microseconds and UTC (Z)
    ]

    for datetime_format in formats:
        try:
            # Try to parse the datetime string using each format
            datetime.strptime(value, datetime_format)
            return True  # If parsing succeeds, the validation passes
        except ValueError:
            continue  # If parsing fails, try the next format

    # If none of the formats worked, raise a ValidationError
    raise ValidationError(f"Invalid datetime format. Acceptable formats are: {', '.join(formats)}")


def validate_date(value: str, formats=None):

    if isinstance(value, date):
        return True

    formats = formats or ["%Y-%m-%d"]  # Default format is YYYY-MM-DD
    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True  # If one format works, the validation succeeds
        except ValueError:
            continue
    raise ValidationError(f"Invalid date format. Acceptable formats are: {', '.join(formats)}")

def validate_time(value: str, formats=None):
    if isinstance(value, (time, datetime.time)):
        return True
    # Define common time formats
    formats = formats or [
        "%H:%M:%S",             # Standard time format
        "%H:%M:%S.%f",          # Time with microseconds
        "%H:%M:%S%z",           # Time with timezone offset
        "%H:%M:%S.%f%z",        # Time with microseconds and timezone offset
        "%H:%M:%SZ",            # Time with UTC (Z for zero-offset)
        "%H:%M:%S.%fZ",         # Time with microseconds and UTC
    ]

    for time_format in formats:
        try:
            # Try to parse the time string using each format
            datetime.strptime(value, time_format)
            return True  # If parsing succeeds, the validation passes
        except ValueError:
            continue  # If parsing fails, try the next format

    # If none of the formats worked, raise a ValidationError
    raise ValidationError(f"Invalid time format. Acceptable formats are: {', '.join(formats)}")

def validate_decimal(value):
    try:
        Decimal(value)
    except ValueError:
        raise ValidationError("Invalid decimal number.")


def validate_boolean(value):
    # Define truthy and falsy values
    truthy_values = {True, 1, "1", "true", "True", "yes", "Yes"}
    falsy_values = {False, 0, "0", "false", "False", "no", "No"}

    # Check if the value is in truthy or falsy sets
    if value in truthy_values or value in falsy_values:
        return True

    # If the value is neither truthy nor falsy, raise a validation error
    raise ValidationError("Invalid boolean value. Accepted values are: True, False, 1, 0, 'true', 'false', 'yes', 'no'.")

def wrap_validator(validator):
    """Wrap a Marshmallow validator to raise ValidationError in case of failure."""
    def wrapper(value):
        try:
            # Call the Marshmallow validator
            out = validator(value)
            if isinstance(out, VE):
                raise ValidationError("Not a valid value.")
        except ValidationError as err:
            # Re-raise the error to match Marshmallow's default behavior
            raise ValidationError(err.messages)
    return wrapper


def validate_by_type(validator_type: str) -> callable:
    """Return a validation function based on the type of validator.

    Args:
        validator_type (str): The type of validator to use.

    Raises:
        ValidationError: If the validation fails.

    Returns:
        callable: The validation function.
    """

    validation_map = {
        "email": wrap_validator(validators.email),
        "url": wrap_validator(validators.url),
        "ipv4": wrap_validator(validators.ipv4),
        "ipv6": wrap_validator(validators.ipv6),
        "mac": wrap_validator(validators.mac_address),
        "slug": wrap_validator(validators.slug),
        "uuid": wrap_validator(validators.uuid),
        "card": wrap_validator(validators.card_number),
        "country_code": wrap_validator(validators.country_code),
        "domain": wrap_validator(validators.domain),
        "md5": wrap_validator(validators.md5),
        "sha1": wrap_validator(validators.sha1),
        "sha256": wrap_validator(validators.sha256),
        "sha512": wrap_validator(validators.sha512),
        "date": lambda value: validate_date(value, formats=["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]),
        "datetime": lambda value: validate_datetime(value, formats=["%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]),
        "time": validate_time,
        "boolean": validate_boolean,
    }
    return validation_map.get(validator_type)
