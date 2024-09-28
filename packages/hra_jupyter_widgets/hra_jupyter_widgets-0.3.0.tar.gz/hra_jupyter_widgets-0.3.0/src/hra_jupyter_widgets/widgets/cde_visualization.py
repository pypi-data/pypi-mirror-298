import json

from traitlets import Dict, Float, Integer, List, Unicode

from ..trait_types import Attribute, Event
from .hra_app import HraAppIframeWidget


def _as_string_or_json(value, _widget) -> str:
    return value if value is None or isinstance(value, str) else json.dumps(value)


class CdeVisualization(HraAppIframeWidget):
    _tag_name = "cde-visualization"
    _scripts = [
        "https://cdn.humanatlas.io/ui/cde-visualization-wc/polyfills.js",
        "https://cdn.humanatlas.io/ui/cde-visualization-wc/main.js",
    ]
    _styles = ["https://cdn.humanatlas.io/ui/cde-visualization-wc/styles.css"]

    nodes = Attribute(
        Unicode() | List(),
        required=True,
        help="Nodes to display, either an url or a list of nodes.",
    ).tag(to_json=_as_string_or_json)
    node_target_key = Attribute(
        Unicode(None, allow_none=True), help="Column name of node targets."
    )
    node_target_value = Attribute(Unicode(None, allow_none=True), help="Anchor node.")
    edges = Attribute(
        Unicode(None, allow_none=True) | List(),
        help="Edges between nodes, either an url or a list of edges.",
    ).tag(to_json=_as_string_or_json)
    max_edge_distance = Attribute(
        Integer(None, allow_none=True),
        help="Max distance between nodes when calculating edges.",
    )
    color_map = Attribute(
        Unicode(None, allow_none=True) | List(), help="Color map url."
    )
    color_map_key = Attribute(
        Unicode(None, allow_none=True), help="Column name of the node targets."
    )
    color_map_value_key = Attribute(
        Unicode(None, allow_none=True), help="Column name of colors."
    )
    metadata = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Metadata displayed in the application.",
    )
    title = Attribute(Unicode(None, allow_none=True), help="Title of the dataset.")
    organ = Attribute(
        Unicode(None, allow_none=True), help="Organ from which the data originates."
    )
    technology = Attribute(
        Unicode(None, allow_none=True), help="Technology used when creating the sample."
    )
    sex = Attribute(Unicode(None, allow_none=True), help="Tissue donor's sex.")
    age = Attribute(Integer(None, allow_none=True), help="Tissue donor's age.")
    thickness = Attribute(Float(None, allow_none=True), help="Sample thickness.")
    pixel_size = Attribute(Integer(None, allow_none=True), help="Sample pixel size.")
    creation_timestamp = Attribute(
        Integer(None, allow_none=True),
        help="Creation timestamp in milliseconds since 00:00:00 UTC - January 1, 1970.",
    )

    on_node_click = Event(
        event_name="nodeClick", help="Event emitted when a cell is clicked."
    )
    on_node_hover = Event(
        event_name="nodeHover",
        help="Event emitted when a cell is hovered over. Emits None when the user stops hovering.",
    )
