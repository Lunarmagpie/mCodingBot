from __future__ import annotations

from typing import TYPE_CHECKING
from re import compile, I

from pincer import Client
from pincer.objects.message import MessageType

if TYPE_CHECKING:
    from pincer.objects import UserMessage


class React:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.rust_search = compile(r"\brust\b", flags=I)

    async def create_reaction(self, message: UserMessage, reaction: str):
        await message._http.put(
            f"/channels/{message.channel_id}/messages/{message.id}/reactions/"
            f"{reaction}/@me",
            None
        )

    @Client.event
    async def on_message(self, message: UserMessage):
        if message.type == MessageType.GUILD_MEMBER_JOIN:
            await self.create_reaction(message, "👋")
            return

        if self.rust_search.findall(message.content) and "🚀" in message.content:
            await self.create_reaction(message, "🚀")


setup = React
