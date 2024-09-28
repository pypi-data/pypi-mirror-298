from __future__ import annotations

import typing as t
from collections import abc

from traitlets import Callable

EventHandler = abc.Callable[[t.Any], None]


class OnEvent(t.Protocol):
    def __call__(self, callback: EventHandler, remove=False) -> None: ...


@t.runtime_checkable
class EventSource(t.Protocol):
    def on_event(
        self, event_name: str, callback: EventHandler, remove=False
    ) -> None: ...


class Event(Callable):
    """A widget method used to register application event listeners."""

    info_text = "an event"

    @property
    def event_name(self) -> str:
        """The html event name.

        Raises:
            AttributeError: If an event name has not been set.
        """
        if self.metadata["event_name"]:
            return self.metadata["event_name"]
        elif self.name:
            return self.name.replace("_", "-").removeprefix("on-")
        else:
            raise AttributeError("Cannot determine an event_name")

    @property
    def properties(self) -> list[str] | None:
        """Properties read from the event object and passed to the listener."""
        return self.metadata["properties"]

    @property
    def _definition(self):
        return {"name": self.event_name, "keys": self.properties}

    def __init__(
        self,
        event_name: str | None = None,
        properties: list[str] | None = None,
        help: str | None = None,
    ) -> None:
        """Declares an event method.

        Args:
            event_name (str | None, optional): Html event name, inferred if not provided.
            properties (list[str] | None, optional): Properties read from the event object. Defaults to None.
            help (str | None, optional): Event help documentation. Defaults to None.
        """
        super().__init__(read_only=True, help=help)
        self.tag(type="event", event_name=event_name, properties=properties)

    def default(self, obj: t.Any = None) -> OnEvent:
        if not isinstance(obj, EventSource):
            raise TypeError("Events must be registered on an event source")

        def on_event(callback: EventHandler, remove=False) -> None:
            obj.on_event(self.event_name, callback, remove)

        if self.name:
            on_event.__name__ = self.name
        return on_event
