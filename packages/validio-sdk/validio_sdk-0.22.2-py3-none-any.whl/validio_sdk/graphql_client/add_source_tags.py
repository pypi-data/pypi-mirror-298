from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class AddSourceTags(BaseModel):
    source_tags_add: "AddSourceTagsSourceTagsAdd" = Field(alias="sourceTagsAdd")


class AddSourceTagsSourceTagsAdd(BaseModel):
    errors: List["AddSourceTagsSourceTagsAddErrors"]


class AddSourceTagsSourceTagsAddErrors(ErrorDetails):
    pass


AddSourceTags.model_rebuild()
AddSourceTagsSourceTagsAdd.model_rebuild()
