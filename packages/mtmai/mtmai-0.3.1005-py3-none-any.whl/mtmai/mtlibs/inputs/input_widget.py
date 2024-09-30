from typing import Any

from pydantic import BaseModel
from typing_extensions import Literal

InputWidgetType = Literal[
    "string",
    "textarea",
    "number",
    "boolean",
    "tags",
    "array",
    "object",
    "select",
    "slider",
    "switch",
]


class InputWidgetBase(BaseModel):
    """
    输入组件的基类, 对应全段标准 html input 组件
    """

    class Config:
        arbitrary_types_allowed = True

    id: str | None = None
    name: str | None = None
    placeholder: str | None = None
    label: str | None = None
    tooltip: str | None = None
    description: str | None = None
    type: InputWidgetType | None = "string"
    placeholder: str | None = None
    value: str | None = None

    # 附加选项，主要因为个别组件仅使用标准 html input 属性时不足以表达必要的参数
    options: dict[str, Any] | None = None


class TextInput(InputWidgetBase):
    """Useful to create a text input."""

    pass


class TextArea(InputWidgetBase):
    """Useful to create a text input."""

    type: InputWidgetType | None = "textarea"
