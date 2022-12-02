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
    def __init__(self, response_body, response_body_parsed):
        # TODO Exception failing on launch due to super args/kwargs
        super().__init__(
            msg="Invalid response body",
            response_body=response_body,
            response_body_parsed=response_body_parsed,
        )
