from __future__ import annotations

from traitlets import Any, Dict, List, Unicode


class AttributeDef(Dict):
    info_text = "an attribute definition"

    def __init__(self, **kwargs):
        kwargs["per_key_traits"] = {
            "name": Unicode(),
            "key": Unicode(allow_none=True),
            "value": Any(allow_none=True),
        }
        super().__init__(**kwargs)


class ElementDef(Dict):
    info_text = "an element definition"

    def __init__(self, **kwargs):
        kwargs["per_key_traits"] = {
            "tag": Unicode(),
            "attributes": List(AttributeDef(), allow_none=True),
            "events": List(EventDef(), allow_none=True),
        }
        super().__init__(**kwargs)

    @classmethod
    def from_script_url(cls, url: str):
        return {
            "tag": "script",
            "attributes": [
                {"name": "src", "value": url},
                {"name": "type", "value": "module"},
            ],
        }

    @classmethod
    def from_style_url(cls, url: str):
        return {
            "tag": "link",
            "attributes": [
                {"name": "href", "value": url},
                {"name": "rel", "value": "stylesheet"},
            ],
        }


class EventDef(Dict):
    info_text = "an event definition"

    def __init__(self, **kwargs):
        kwargs["per_key_traits"] = {
            "name": Unicode(),
            "keys": List(Unicode(), allow_none=True),
        }
        super().__init__(**kwargs)


class StyleDef(Dict):
    info_text = "a style definition"

    def __init__(self, **kwargs):
        kwargs["per_key_traits"] = {
            "name": Unicode(),
            "key": Unicode(allow_none=True),
            "value": Any(allow_none=True),
        }
        super().__init__(**kwargs)
