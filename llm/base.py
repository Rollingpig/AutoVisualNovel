from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypedDict

MessageRole = Literal["system", "user", "assistant"]


class MessageDict(TypedDict):
    role: MessageRole
    content: str


@dataclass
class Message:
    """OpenAI Message object containing a role and the message content"""

    role: MessageRole
    content: str

    def __init__(self, role: MessageRole, content: str):
        self.role = role
        self.content = content

    def raw(self) -> MessageDict:
        return {"role": self.role, "content": self.content}


@dataclass
class ChatSequence:
    """Utility container for a chat sequence"""

    messages: list[Message] = field(default_factory=list)

    def __getitem__(self, i: int):
        return self.messages[i]

    def append(self, message: Message):
        return self.messages.append(message)

    def raw(self) -> list[MessageDict]:
        return [message.raw() for message in self.messages]
