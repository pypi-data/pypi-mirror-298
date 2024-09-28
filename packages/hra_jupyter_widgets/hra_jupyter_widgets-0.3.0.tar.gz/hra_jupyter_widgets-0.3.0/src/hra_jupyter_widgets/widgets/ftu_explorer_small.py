from traitlets import Dict, Unicode

from ..trait_types import Attribute, Event
from ._stylesheets import Font, Material
from .hra_app import HraAppIframeWidget

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ftu-ui-small-wc/"
_DEFAULT_SUMMARIES = "assets/TEMP/ftu-cell-summaries.jsonld"
_DEFAULT_DATASETS = "assets/TEMP/ftu-datasets.jsonld"


class FtuExplorerSmall(HraAppIframeWidget):
    """Displays the small version of HRA FTU explorer."""

    _tag_name = "hra-ftu-ui-small"
    _scripts = ["https://cdn.humanatlas.io/ui/ftu-ui-small-wc/wc.js"]
    _styles = [
        Font.Inter,
        Material.Icons,
        Material.Symbols,
        "https://cdn.humanatlas.io/ui/ftu-ui-small-wc/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF, read_only=True))

    selected_illustration = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Url, illustration id, or illustration object to display.",
    )
    illustrations = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Illustration objects used when an id is used to select an illustration.",
    )
    summaries = Attribute(
        Unicode(_DEFAULT_SUMMARIES) | Dict(), help="Cell data summaries."
    )
    datasets = Attribute(Unicode(_DEFAULT_DATASETS) | Dict(), help="Data sources.")

    on_illustration_selected = Event(
        help="Event emitted when the user selects a different illustration."
    )
    on_cell_click = Event(help="Event emitted when a cell is clicked.")
    on_cell_hover = Event(
        help="Event emitted when a cell is hovered over. Emits None when the user stops hovering."
    )
