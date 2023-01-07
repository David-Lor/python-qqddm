from typing import List, Set, Optional

import pydantic

from ..utils import get_uuid4


class AIProcessorRequestBody(pydantic.BaseModel):

    class Extra(pydantic.BaseModel):

        class DataReport(pydantic.BaseModel):
            parent_trace_id: str = pydantic.Field(default_factory=get_uuid4)
            root_channel: str = ""
            level: int = 0

        version: int = 2
        language: str = "en"
        platform: str = "web"
        face_rects: list = []
        data_report: DataReport = pydantic.Field(default_factory=DataReport)

    busiId: str = "different_dimension_me_img_entry"
    images: List[str]
    extra: Optional[str] = None


class AIProcessorResponseBody(pydantic.BaseModel):

    class Extra(pydantic.BaseModel):
        img_urls: Set[pydantic.AnyHttpUrl]

    code: int
    msg: str
    extra: Optional[str] = None

    @property
    def valid(self):
        return self.code == 0

    @property
    def extra_parsed(self):
        return self.Extra.parse_raw(self.extra) if self.extra else None
