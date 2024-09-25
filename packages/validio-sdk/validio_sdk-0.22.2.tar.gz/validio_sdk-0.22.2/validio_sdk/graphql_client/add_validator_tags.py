from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class AddValidatorTags(BaseModel):
    validator_tags_add: "AddValidatorTagsValidatorTagsAdd" = Field(
        alias="validatorTagsAdd"
    )


class AddValidatorTagsValidatorTagsAdd(BaseModel):
    errors: List["AddValidatorTagsValidatorTagsAddErrors"]


class AddValidatorTagsValidatorTagsAddErrors(ErrorDetails):
    pass


AddValidatorTags.model_rebuild()
AddValidatorTagsValidatorTagsAdd.model_rebuild()
