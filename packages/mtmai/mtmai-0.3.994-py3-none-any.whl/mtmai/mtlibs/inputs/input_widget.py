from pydantic import BaseModel
from typing_extensions import Literal

InputWidgetType = Literal["string", "number", "boolean", "tags", "array", "object"]


class InputWidgetBase(BaseModel):
    id: str | None = None
    name: str | None = None
    placeholder: str | None = None
    label: str
    tooltip: str | None = None
    description: str | None = None
    type: InputWidgetType = "string"


class TextInput(InputWidgetBase):
    """Useful to create a text input."""

    pass
