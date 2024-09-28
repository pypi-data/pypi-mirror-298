from traitlets import Dict, Unicode

from ..trait_types import Attribute, Event
from .hra_app import HraAppWidget

_DEFAULT_ILLUSTRATIONS = "https://cdn.humanatlas.io/digital-objects/graph/2d-ftu-illustrations/latest/assets/2d-ftu-illustrations.jsonld"


class MedicalIllustration(HraAppWidget):
    """Displays the HRA medical illustration application."""

    _tag_name = "hra-medical-illustration"
    _scripts = ["https://cdn.humanatlas.io/ui/medical-illustration/wc.js"]
    _styles = ["https://cdn.humanatlas.io/ui/medical-illustration/styles.css"]

    selected_illustration = Attribute(
        Unicode() | Dict(),
        required=True,
        help="Url, illustration id, or illustration object to display.",
    )
    illustrations = Attribute(
        Unicode(_DEFAULT_ILLUSTRATIONS) | Dict(),
        help="Illustration objects used when an id is used to select an illustration.",
    )
    highlight = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Illustration id or illustration object to highlight.",
    )

    on_cell_click = Event(help="Event emitted when a cell is clicked.")
    on_cell_hover = Event(
        help="Event emitted when a cell is hovered over. Emits None when the user stops hovering."
    )
