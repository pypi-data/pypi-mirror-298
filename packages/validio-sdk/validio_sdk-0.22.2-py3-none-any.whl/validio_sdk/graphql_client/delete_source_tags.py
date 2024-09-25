from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteSourceTags(BaseModel):
    source_tags_delete: "DeleteSourceTagsSourceTagsDelete" = Field(
        alias="sourceTagsDelete"
    )


class DeleteSourceTagsSourceTagsDelete(BaseModel):
    errors: List["DeleteSourceTagsSourceTagsDeleteErrors"]


class DeleteSourceTagsSourceTagsDeleteErrors(ErrorDetails):
    pass


DeleteSourceTags.model_rebuild()
DeleteSourceTagsSourceTagsDelete.model_rebuild()
