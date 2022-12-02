import base64
import threading
from typing import Optional, List

import httpx
import pydantic

from .utils import choose
from .models import qqddm_api
from .models.exceptions import qqddm_api as qqddm_api_exceptions


class BaseAnimeConverter(pydantic.BaseModel):
    # TODO Document configuration attributes on docstring

    # Request settings that will override all the per-request settings
    global_request_timeout_seconds: Optional[float] = None
    global_proxy: Optional[str] = None

    # Settings for Generate requests (send a picture and convert to an anime avatar)
    generate_request_url: str = "https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process"
    generate_request_timeout_seconds: float = 30
    generate_proxy: Optional[str] = None

    # Settings for Download requests (download generated pictures)
    download_request_timeout_seconds: float = 20
    download_proxy: Optional[str] = None

    class Config:
        validate_assignment = True

    @staticmethod
    def _get_request_body(picture: bytes):
        picture_b64 = base64.b64encode(picture).decode()
        return qqddm_api.AIProcessorRequestBody(
            images=[picture_b64],
            # extra=qqddm_api.AIProcessorRequestBody.Extra(
            #
            # ).json(),
        )


class AnimeConverter(BaseAnimeConverter):
    """Synchronous AnimeConverter."""

    def convert(
            self,
            picture: bytes
    ) -> "AnimeResult":
        """Convert the given `picture` file (read as bytes) by passing it to QQ's Different Dimension Me AI.

        Returns an `AnimeResult` object, including the URLs of the resulting pictures.
        """

        request_body = self._get_request_body(picture=picture)
        r = self._request(
            request_timeout_seconds=choose(self.global_request_timeout_seconds, self.generate_request_timeout_seconds),
            proxy=choose(self.global_proxy, self.generate_proxy),
            method="POST",
            url=self.generate_request_url,
            json=request_body.dict(),
        )
        r.raise_for_status()

        response = qqddm_api.AIProcessorResponseBody.parse_raw(r.content)
        if not response.valid:
            raise qqddm_api_exceptions.InvalidQQDDMApiResponseException(
                response_body=r.text,
                response_body_parsed=response,
            )

        return AnimeResult(
            pictures_urls=response.extra_parsed.img_urls,
        )

    def download(
            self,
            result: "AnimeResult",
    ) -> List[bytes]:
        """Download all the pictures from an `AnimeResult` object, parallely.

        Returns a list where each element is each downloaded picture as bytes,
        in the same order as `AnimeResult.pictures_urls` list.
        """

        pictures = [None for _ in range(len(result.pictures_urls))]
        threads = [
            threading.Thread(
                target=self._download_one_work(
                    download_url=picture_url,
                    results_list=pictures,
                    results_list_index=i,
                )
            )
            for i, picture_url in enumerate(result.pictures_urls)
        ]

        [th.start() for th in threads]
        [th.join() for th in threads]
        # noinspection PyTypeChecker
        return pictures

    def download_one(
            self,
            download_url: str,
    ) -> bytes:
        """Request GET the given URL, downloading and returning the response bytes.
        """
        r = self._request(
            request_timeout_seconds=choose(self.global_request_timeout_seconds, self.download_request_timeout_seconds),
            proxy=choose(self.global_proxy, self.download_proxy),
            method="GET",
            url=download_url,
        )
        r.raise_for_status()
        return r.content

    def _download_one_work(
            self,
            download_url: str,
            results_list: list,
            results_list_index: int,
    ):
        r = self.download_one(download_url=download_url)
        results_list[results_list_index] = r

    @staticmethod
    def _request(
            request_timeout_seconds: float,
            proxy: Optional[str],
            **request_kwargs,
    ) -> httpx.Response:
        with httpx.Client(proxies=proxy, timeout=request_timeout_seconds) as http:
            return http.request(**request_kwargs)


class AnimeResult(pydantic.BaseModel):

    pictures_urls: List[pydantic.AnyHttpUrl]
