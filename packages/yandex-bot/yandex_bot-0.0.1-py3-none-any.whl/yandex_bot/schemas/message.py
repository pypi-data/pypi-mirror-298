from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Chat(BaseModel):
    type: str
    id: str | None = None


class FromUser(BaseModel):
    id: str
    display_name: str
    login: str
    robot: bool


class ForwardedMessage(BaseModel):
    message_id: int
    timestamp: int
    chat: Chat
    from_: FromUser = Field(..., alias="from")
    text: Optional[str]


class Sticker(BaseModel):
    id: str
    set_id: str


class File(BaseModel):
    id: str
    name: str
    size: int


class Image(BaseModel):
    file_id: str
    width: int
    height: int
    size: Optional[int]
    name: Optional[str]


class Message(BaseModel):
    message_id: int
    timestamp: int
    chat: Chat
    from_: FromUser = Field(..., alias="from")
    update_id: int
    text: str | None = None
    forwarded_messages: List[ForwardedMessage] | None = None
    sticker: Sticker | None = None
    images: List[List[Image]] | None = None
    file: File | None = None


class PolingResponse(BaseModel):
    updates: List[Message] | None = []
    ok: bool
    description: str | None = ""
