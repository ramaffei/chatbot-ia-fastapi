from typing import Literal

from fastapi import Query
from pydantic import Field, field_validator
from pydantic.alias_generators import to_snake
from schemas.base import CamelModel


class OutputPagination(CamelModel):
    page: int | None = Field(
        default=1, ge=1, description="Current page that's being fetch.", examples=[1]
    )
    page_size: int | None = Field(
        default=10,
        ge=1,
        description="Amount of items that the current page will have.",
        examples=[10],
    )
    total: int = Field(
        default=0,
        description="Total amount of registers taken into account the used filters.",
    )

    # this field is overwritten by the child classes
    data: list = Field(default=[], description="The items that will be listed.")


class InputPagination(CamelModel):
    page: int | None = Field(
        Query(
            default=1,
            ge=1,
            description="Current page that's being fetch.",
            examples=[1],
        )
    )
    page_size: int | None = Field(
        Query(
            default=10,
            ge=1,
            description="Amount of items that the current page will have.",
            examples=[10],
        )
    )
    sort_field: str | None = Field(
        Query(
            default=None,
            include_in_schema=False,
            description="Field that will be used to order the result. If not available, order will be ignored. If ignored, model decides it's default order",
            examples=["name"],
        )
    )
    sort: Literal["ASC", "DESC"] | None = Field(
        Query(
            default="DESC",
            include_in_schema=False,
            description="Order that will be applied to the provided sortField. Value must be in UPPERCASE",
            examples=["ASC", "DESC"],
        )
    )

    def pagination_params(self) -> dict:
        return {
            "page": self.page,
            "page_size": self.page_size,
            "sort_field": self.sort_field,
            "sort": self.sort,
        }

    def page_and_size(self) -> dict:
        return {
            "page": self.page,
            "page_size": self.page_size,
        }

    # Child classes add their own fields to filter

    # NOTE: if @classmethod goes first, validator does not work.
    @field_validator("sort_field", mode="after")
    @classmethod
    def validate_sort_field(cls, field: str | None) -> str | None:
        """Converts the field to snake case"""
        if field is not None:
            return to_snake(field)
        return field
