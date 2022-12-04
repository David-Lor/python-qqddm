from typing import List, Optional

import pydantic


class AIProcessorRequestBody(pydantic.BaseModel):

    class Extra(pydantic.BaseModel):
        version: Optional[int] = None
        platform: str = "web"

    busiId: str = "ai_painting_anime_entry"
    images: List[str]
    extra: Optional[str] = None


class AIProcessorResponseBody(pydantic.BaseModel):

    class Extra(pydantic.BaseModel):
        video_urls: List[pydantic.AnyHttpUrl]
        img_urls: List[pydantic.AnyHttpUrl]

    code: int
    msg: str
    extra: Optional[str] = None

    @property
    def valid(self):
        return self.code == 0

    @property
    def extra_parsed(self):
        return self.Extra.parse_raw(self.extra) if self.extra else None
