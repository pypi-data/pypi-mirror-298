import uuid
from datetime import datetime

from sqlmodel import JSON, Column, Field

from mtmai.models.base_model import MtmBaseSqlModel


class ChatThread(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=True)
    user_id: str = Field(foreign_key="user.id", nullable=True, ondelete="CASCADE")
    user_identifier: str = Field(nullable=True)
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    meta: dict | None = Field(default={}, sa_column=Column(JSON))

    _upsert_index_elements = {"id"}


class ChatStep(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    type: str = Field(max_length=255)
    thread_id: uuid.UUID = Field(...)
    parent_id: uuid.UUID | None = Field(default=None)
    disable_feedback: bool = Field(...)
    streaming: bool = Field(...)
    wait_for_answer: bool | None = Field(default=None)
    is_error: bool | None = Field(default=None)
    meta: dict | None = Field(default=None, sa_column=Column(JSON))
    tags: list[str] | None = Field(default=[], sa_column=Column(JSON))
    input: str | None = Field(default=None)
    output: str | None = Field(default=None)
    start: datetime | None = Field(default=None)
    end: datetime | None = Field(default=None)
    generation: dict | None = Field(default=None, sa_column=Column(JSON))
    show_input: str | None = Field(default=None)
    language: str | None = Field(default=None)
    indent: int | None = Field(default=None)

    _upsert_index_elements = {"id"}

    # #############################################################################################
    # # Specifies the set of index elements which represent the ON CONFLICT target
    # UPSERT_INDEX_ELEMENTS: ClassVar[set[str]] = {"id"}

    # # Specifies the set of fields to exclude from updating in the resulting
    # # UPSERT statement
    # UPSERT_EXCLUDE_FIELDS: ClassVar[set[str]] = set()

    # def upsert(self):
    #     """Returns an UPSERT statement"""
    #     exclude_fields = self.UPSERT_EXCLUDE_FIELDS.copy()

    #     # Common fields which we should exclude when updating.
    #     exclude_fields.add("id")
    #     exclude_fields.add("created_at")

    #     # Dump the model and exclude the specified fields during update.
    #     obj_dict = self.model_dump()
    #     to_update = obj_dict.copy()
    #     for field in exclude_fields:
    #         _ = to_update.pop(field, None)

    #     stmt = insert(self.__class__).values(obj_dict)
    #     stmt = stmt.on_conflict_do_update(
    #         index_elements=self.UPSERT_INDEX_ELEMENTS,
    #         set_=to_update,
    #     )

    #     return stmt


class ChatElement(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID | None = Field(default=None)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None)
    chainlit_key: str | None = Field(default=None)
    name: str = Field(...)
    display: str | None = Field(default=None)
    object_key: str | None = Field(default=None)
    size: str | None = Field(default=None)
    page: int | None = Field(default=None)
    language: str | None = Field(default=None)
    for_id: uuid.UUID | None = Field(default=None)
    mime: str | None = Field(default=None)

    _upsert_index_elements = {"id"}


class ChatFeedback(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    for_id: uuid.UUID = Field(...)
    thread_id: uuid.UUID = Field(...)
    value: int = Field(...)
    comment: str | None = Field(default=None)

    _upsert_index_elements = {"id"}


class ChatProfile(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(...)
    description: str = Field(...)
    icon: str | None = Field(default=None)
    default: bool | None = Field(default=False)
    # starters: list[dict] = Field(default=[])
    starters: list[dict] | None = Field(default=None, sa_column=Column(JSON))
