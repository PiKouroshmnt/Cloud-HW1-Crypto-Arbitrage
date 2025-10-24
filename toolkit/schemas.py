"""Module contains base schemas for the application."""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all request and response models."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
        use_enum_values=True,
    )
