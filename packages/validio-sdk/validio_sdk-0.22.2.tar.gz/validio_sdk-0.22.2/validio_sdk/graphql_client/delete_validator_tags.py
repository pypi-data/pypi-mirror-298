from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteValidatorTags(BaseModel):
    validator_tags_delete: "DeleteValidatorTagsValidatorTagsDelete" = Field(
        alias="validatorTagsDelete"
    )


class DeleteValidatorTagsValidatorTagsDelete(BaseModel):
    errors: List["DeleteValidatorTagsValidatorTagsDeleteErrors"]


class DeleteValidatorTagsValidatorTagsDeleteErrors(ErrorDetails):
    pass


DeleteValidatorTags.model_rebuild()
DeleteValidatorTagsValidatorTagsDelete.model_rebuild()
