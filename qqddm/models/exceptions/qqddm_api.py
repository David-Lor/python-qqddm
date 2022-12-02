from typing import Optional

from .base import BaseQQDDMException
from ..qqddm_api import AIProcessorResponseBody


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
