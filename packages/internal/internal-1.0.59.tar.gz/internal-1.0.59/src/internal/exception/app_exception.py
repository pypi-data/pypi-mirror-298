from fastapi import status
from .base_exception import InternalBaseException


class AccountLengthOrFormatException(InternalBaseException):
    code = "error_account_length_or_format"
    message = "Account only allow alphanumeric 30 characters"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)

class AccountNullPointException(InternalBaseException):
    code = "error_account_not_be_null"
    message = "Account can not be null"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)


class PasswordNullPointException(InternalBaseException):
    code = "error_password_not_be_null"
    message = "Password can not be null"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)


class BrandNullPointException(InternalBaseException):
    code = "error_brand_not_be_null"
    message = "Brand can not be null"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)

class PlateNoFormatException(InternalBaseException):
    code = "error_plate_no_format"
    message = "Plate numbers only allow alphanumeric 6 or 7 characters"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)

class VinLengthOrFormatException(InternalBaseException):
    code = "error_vin_length_or_format"
    message = "VIN only allow alphanumeric 7 or 17 characters"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)

class PhoneFormatException(InternalBaseException):
    code = "error_phone_format"
    message = "Phone only allow numeric"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)