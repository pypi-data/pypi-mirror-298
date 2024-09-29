from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from mtmai.chainlit.chat_settings import ThreadForm
from mtmai.chainlit.context import context


class ThreadUIState(BaseModel):
    """ThreadView 的UI 状态"""

    enableChat: bool = True
    enableScrollToBottom: bool = True
    title: str = ""
    description: str = ""
    icons: str = ""
    layout: str = ""
    theme: str = ""
    threadForm: ThreadForm | None = None

    # def settings(self) -> dict[str, Any]:
    #     return {input_widget.id: input_widget.initial for input_widget in self.inputs}

    async def send(self) -> dict[str, Any]:
        # uiState = self.settings()
        # context.emitter.set_chat_settings(settings)

        # inputs_content = [input_widget.to_dict() for input_widget in self.inputs]
        await context.emitter.emit("thread_ui_state", jsonable_encoder(self))

        return self
