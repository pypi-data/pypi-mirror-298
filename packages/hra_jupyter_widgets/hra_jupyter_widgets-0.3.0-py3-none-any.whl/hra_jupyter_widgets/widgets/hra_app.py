from __future__ import annotations

import collections
import collections.abc
import pathlib
import typing as t

import anywidget
import ipywidgets
from traitlets import Bool, Instance, List, Unicode, default

from ..trait_types import Attribute, ElementDef, Event


class HraAppWidget(anywidget.AnyWidget):
    """Base class for hra application widgets.

    Attributes:
        width (string): Width of the widget (css value).
        height (string): Height of the widget (css value).
    """

    _esm = pathlib.Path(__file__).resolve().parent.parent / "static" / "hra_app.js"

    _tag_name: t.ClassVar[str]
    _scripts: t.ClassVar[list[str]]
    _styles: t.ClassVar[list[str]]

    _use_iframe = Bool(
        False,
        help="Whether to create an iframe for the application",
    ).tag(sync=True)
    _element = ElementDef(
        read_only=True,
        help="Main application element definition",
    ).tag(sync=True)
    _meta_elements = List(
        ElementDef(),
        read_only=True,
        help="Meta element definitions",
    ).tag(sync=True)
    _event_listeners = Instance(
        collections.defaultdict,
        (ipywidgets.CallbackDispatcher,),
        read_only=True,
        help="Event callback listeners",
    )

    # TODO improve width & height types using custom css traitlets
    width = Unicode("100%", help="Widget width").tag(sync=True)
    height = Unicode("auto", help="Widget height").tag(sync=True)

    @property
    def __attribute_traits(self) -> collections.abc.Iterable[Attribute]:
        return self.traits(type="attribute").values()

    @property
    def __event_traits(self) -> collections.abc.Iterable[Event]:
        return self.traits(type="event").values()

    @default("_element")
    def _element_default(self):
        return {
            "tag": self._tag_name,
            "attributes": [trait._definition for trait in self.__attribute_traits],
            "styles": [],
            "events": [trait._definition for trait in self.__event_traits],
        }

    @default("_meta_elements")
    def _meta_elements_default(self):
        scripts = (ElementDef.from_script_url(url) for url in self._scripts)
        styles = (ElementDef.from_style_url(url) for url in self._styles)
        return [*scripts, *styles]

    def __init__(self, **kwargs: t.Any) -> None:
        """Initializes the widget.
        Ensures all required attributes are provided as arguments and
        starts event processing.
        """

        self.__check_required_attributes(kwargs)
        super().__init__(**kwargs)
        self.on_msg(self.__handle_event_msg)

    def on_event(
        self,
        event_name: str,
        callback: t.Callable[[t.Any], t.Any],
        remove=False,
    ) -> None:
        """Register an event listener.

        Args:
            event_name (str): Event name.
            callback (t.Callable[[t.Any], t.Any]): Listener function, called with the event data.
            remove (bool, optional): Whether to remove the listener. Defaults to False.
        """

        self._event_listeners[event_name].register_callback(callback, remove)

    def __check_required_attributes(self, kwargs: dict[str, t.Any]) -> None:
        missing: list[str] = []
        for name in self.trait_names(type="attribute", required=True):
            if name not in kwargs:
                missing.append(name)

        if missing:
            raise AttributeError(f"Missing required arguments: {missing}")

    def __handle_event_msg(
        self, _widget: t.Any, content: t.Any, _buffers: t.Any
    ) -> None:
        if isinstance(content, dict) and "event" in content:
            event_name = content["event"]
            data = content.get("data")
            self._event_listeners[event_name](data)


class HraAppIframeWidget(HraAppWidget):
    """Base class for hra application widgets that renders
    the application inside an iframe element for better isolation.

    The iframe has a default height of 1000px.
    """

    @default("_use_iframe")
    def _use_iframe_default(self) -> bool:
        return True

    @default("height")
    def _height_default(self) -> str:
        return "1000px"
