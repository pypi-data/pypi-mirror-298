from typing import Any, List

from pydantic import BaseModel

from mtmai.chainlit.context import context
from mtmai.chainlit.input_widget import InputWidget


class ThreadUIState(BaseModel):
    """发送Html 表单 向用户询问要执行任务的相关参数"""

    enableChat: bool = True
    enableScrollToBottom: bool = True
    title: str = "ThreadForm"
    description: str = "ThreadForm"
    inputs: List[InputWidget]

    # def settings(self) -> dict[str, Any]:
    #     return {input_widget.id: input_widget.initial for input_widget in self.inputs}

    async def send(self) -> dict[str, Any]:
        uiState = self.settings()
        # context.emitter.set_chat_settings(settings)

        # inputs_content = [input_widget.to_dict() for input_widget in self.inputs]
        await context.emitter.emit("thread_ui_state", uiState)

        return uiState
