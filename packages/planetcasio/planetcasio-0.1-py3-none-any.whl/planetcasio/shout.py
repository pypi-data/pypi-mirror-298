#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2024 Thomas Touhey <thomas@touhey.fr>
#
# This software is governed by the CeCILL-C license under French law and
# abiding by the rules of distribution of free software. You can use, modify
# and/or redistribute the software under the terms of the CeCILL-C license
# as circulated by CEA, CNRS and INRIA at the following
# URL: https://cecill.info
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean
# that it is complicated to manipulate, and that also therefore means that it
# is reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C license and that you accept its terms.
# *****************************************************************************
"""Planète Casio's shoutbox interactions."""

from __future__ import annotations

from asyncio import sleep
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from time import monotonic
from typing import Literal, Union

from pydantic import AwareDatetime, BaseModel
from typing_extensions import TypeAlias

from .transport import BaseClient, Feature


class _ReadResponseMessage(BaseModel):
    """Message in read response."""

    id: int
    """Identifier of the message."""

    posted: int
    """UNIX timestamp at which the message was posted."""

    author: str
    """Username of the message author."""

    groupname: str
    """Name of the group."""

    groupcss: str
    """CSS of the group."""

    content: str
    """Message content.

    This depends on the source:

    * If the source is 'SHOUTBOX', this is the message in the requested format.
    * If the source is 'DELETION', this is the stringified ID of the message to
      delete.
    """

    source: Literal["SHOUTBOX", "DELETION"]
    """Message source."""


class _ReadResponse(BaseModel):
    """Read response."""

    erreur: int
    """Error code."""

    username: str | None
    """Current username."""

    messages: list[_ReadResponseMessage]
    """Messages."""

    time: int
    """Current time on the server, as a UNIX timestamp."""

    candelete: bool
    """Whether the current user can delete messages."""


class MessagePosted(BaseModel):
    """A message was posted by a user."""

    id: int
    """Identifier of the posted message."""

    username: str
    """Username of the posted message."""

    content: str
    """Content of the posted message."""

    at: AwareDatetime
    """Date and time at which the message was posted."""


class MessageDeleted(BaseModel):
    """A message was deleted by a user."""

    id: int
    """Identifier of the message that has been deleted."""

    at: AwareDatetime
    """Date and time at which the message was deleted."""


Event: TypeAlias = Union[MessagePosted, MessageDeleted]
"""Event emitted on a shoutbox channel.

See :py:class:`Channel` for more information.
"""


class Channel(Feature):
    """Shoutbox channel.

    Iterating over this class yields events occuring in the channel.
    For example, in order to read messages from the ``hs`` channel:

    .. code-block:: python

        from planetcasio.client import Client
        from planetcasio.shout import MessagePosted

        async with Client(auth=("myusername", "mypassword")) as client:
            channel = await client.get_channel("hs")
            async for event in channel:
                if isinstance(event, MessagePosted):
                    print(f"{event.username}: {event.content}")
    """

    __slots__ = (
        "_delay",
        "_format",
        "_last_read",
        "_messages",
        "_name",
        "_since",
    )

    _delay: int
    """Minimum delay between two read operations, in seconds."""

    _format: str
    """Format of the messages to request from the shoutbox."""

    _last_read: float | None
    """Time of last read in the monotonic clock."""

    _messages: list[_ReadResponseMessage]
    """Last received messages."""

    _name: str
    """Name of the channel."""

    _since: int
    """Timestamp of the last timestamp from which to read messages."""

    def __init__(
        self,
        client: BaseClient,
        name: str,
        /,
        *,
        format: str,
    ) -> None:
        Feature.__init__(self, client)
        self._delay = 5
        self._format = format
        self._last_read = None
        self._messages = []
        self._name = name
        self._since = 0

    def __aiter__(self) -> AsyncIterator[Event]:
        return self

    async def __anext__(self) -> Event:
        while True:
            message = self._get_next_event()
            if message is not None:
                return message

            if self._last_read is not None:
                delta = monotonic() - self._last_read
                if delta < self._delay:
                    await sleep(self._delay - delta)

            response = await self.transport.request_api(
                "Fr/shoutbox/api/read",
                params={
                    "since": str(self._since),
                    "format": self._format,
                    "channel": self._name,
                },
                model=_ReadResponse,
            )
            self._update(response)

    def _update(self, response: _ReadResponse, /) -> None:
        """Update the current state based on the provided response.

        :param response: Response to use to update the current state.
        """
        if response.erreur != 0:
            raise ValueError(f"Error {response.erreur} has occurred.")

        if response.messages:
            self._messages.extend(response.messages)
            self._since = response.messages[-1].id

        self._last_read = monotonic()

    def _get_next_event(self, /) -> Event | None:
        """Get the next event based on the current message cache.

        :return: Next event if available, or :py:data:`None` otherwise.
        """
        while self._messages:
            message = self._messages.pop(0)

            if message.source == "SHOUTBOX":
                return MessagePosted(
                    id=message.id,
                    username=message.author,
                    content=message.content,
                    at=datetime.fromtimestamp(message.posted, timezone.utc),
                )
            elif message.source == "DELETION":
                return MessageDeleted(
                    id=int(message.content),
                    at=datetime.fromtimestamp(message.posted, timezone.utc),
                )

        return None

    async def post(self, message: str, /) -> None:
        """Post a message in the channel.

        :param message: Message to post, in BBCode.
        """
        await self.transport.check_auth()
        response = await self.transport.request_api(
            "Fr/shoutbox/api/post",
            form_data={
                "message": message,
                "since": str(self._since),
                "format": self._format,
                "channel": self._name,
            },
            model=_ReadResponse,
        )
        self._update(response)


class Shout(Feature):
    """Shoutbox client."""

    __slots__ = ()

    async def get_channel(
        self,
        name: str,
        /,
        *,
        format: Literal["html", "text", "bbcode", "irc"] = "html",
    ) -> Channel:
        """Get a channel with a given name.

        :param name: Name of the channel to get.
        :param format: Format to request for the messages.
        :return: Channel with the provided name.
        """
        return Channel(self.client, name, format=format)
