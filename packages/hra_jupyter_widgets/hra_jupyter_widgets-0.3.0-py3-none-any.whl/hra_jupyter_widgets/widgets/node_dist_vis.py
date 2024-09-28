from __future__ import annotations

import json
import typing as t

from traitlets import Integer, List, Unicode

from ..trait_types import Attribute
from .hra_app import HraAppWidget


def _as_string_or_json(value, _widget) -> str:
    return value if value is None or isinstance(value, str) else json.dumps(value)


class NodeDistVis(HraAppWidget):
    """Displays the HRA node distance visualization."""

    _tag_name = "hra-node-dist-vis"
    _scripts = [
        "https://cdn.jsdelivr.net/gh/cns-iu/hra-node-dist-vis/docs/hra-node-dist-vis.wc.js"
    ]
    _styles = []

    nodes = Attribute(
        Unicode() | List(),
        required=True,
        help="Nodes to display, either an url or a list of nodes.",
    ).tag(to_json=_as_string_or_json)
    node_target_key = Attribute(
        Unicode(), required=True, help="Column name of node targets."
    )
    node_target_value = Attribute(Unicode(), required=True, help="Anchor node.")
    edges = Attribute(
        Unicode(None, allow_none=True) | List(),
        help="Edges between nodes, either an url or a list of edges.",
    ).tag(to_json=_as_string_or_json)
    max_edge_distance = Attribute(
        Integer(), help="Max distance between nodes when calculating edges."
    )
    color_map = Attribute(
        Unicode(None, allow_none=True) | List(), help="Color map url."
    )
    color_map_key = Attribute(
        Unicode(None, allow_none=True), help="Column name of the node targets."
    )
    color_map_data = Attribute(
        Unicode(None, allow_none=True), help="Column name of colors."
    )
    selection = Attribute(
        List(default_value=None, allow_none=True), help="Selection of nodes to display."
    )

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        if "edges" not in kwargs and "max_edge_distance" not in kwargs:
            raise AttributeError(
                "max_edge_distance must be set when not providing edges"
            )

        if "color_map" in kwargs:
            if "color_map_key" not in kwargs:
                raise AttributeError(
                    "color_map_key must be set when providing a color_map"
                )
            if "color_map_data" not in kwargs:
                raise AttributeError(
                    "color_map_data must be set when providing a color_map"
                )

        super().__init__(*args, **kwargs)
