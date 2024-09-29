from typing import Any

from pydantic import BaseModel
from typing_extensions import Literal

InputWidgetType = Literal[
    "string", "number", "boolean", "tags", "array", "object", "select"
]


class InputWidgetBase(BaseModel):
    id: str | None = None
    name: str | None = None
    placeholder: str | None = None
    label: str | None = None
    tooltip: str | None = None
    description: str | None = None
    type: InputWidgetType | None = "string"
    placeholder: str | None = None

    # 附加选项，主要因为个别组件仅使用标准 html input 属性时不足以表达必要的参数
    options: dict[str, Any] | None = None


class TextInput(InputWidgetBase):
    """Useful to create a text input."""

    pass
