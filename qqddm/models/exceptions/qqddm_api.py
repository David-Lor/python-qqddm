from typing import Optional

from .base import BaseQQDDMException
from ..qqddm_api import AIProcessorResponseBody

__all__ = [
    "BaseQQDDMApiException", "InvalidQQDDMApiResponseException", "IllegalPictureQQDDMApiResponseException",
    "RESPONSE_CODES_EXCEPTIONS"
]


class BaseQQDDMApiException(BaseQQDDMException):
    response_body: str
    response_body_parsed: Optional[AIProcessorResponseBody]

    def __init__(self, msg, response_body, response_body_parsed):
        super().__init__(msg)
        self.response_body = response_body
        self.response_body_parsed = response_body_parsed


class InvalidQQDDMApiResponseException(BaseQQDDMApiException):
    error_msg = "Invalid response body"

    def __init__(self, response_body, response_body_parsed):
        super().__init__(
            msg=self.error_msg,
            response_body=response_body,
            response_body_parsed=response_body_parsed,
        )


class IllegalPictureQQDDMApiResponseException(InvalidQQDDMApiResponseException):
    error_msg = "Illegal picture"


class VolumnLimitQQDDMApiResponseException(InvalidQQDDMApiResponseException):
    error_msg = "API rate limited or picture too big"


class AuthFailedQQDDMApiResponseException(InvalidQQDDMApiResponseException):
    error_msg = "Auth failed (the API may have changed and the library is currently not compatible)"


class NotAllowedCountryQQDDMApiResponseException(InvalidQQDDMApiResponseException):
    error_msg = "The current country is blocked by the API"


class NoFaceInPictureQQDDMApiResponseException(InvalidQQDDMApiResponseException):
    error_msg = "The picture does not have a valid face"


RESPONSE_CODES_EXCEPTIONS = {
    2114: IllegalPictureQQDDMApiResponseException,
    2111: VolumnLimitQQDDMApiResponseException,
    -2111: AuthFailedQQDDMApiResponseException,
    2119: NotAllowedCountryQQDDMApiResponseException,
    1001: NoFaceInPictureQQDDMApiResponseException,
}
