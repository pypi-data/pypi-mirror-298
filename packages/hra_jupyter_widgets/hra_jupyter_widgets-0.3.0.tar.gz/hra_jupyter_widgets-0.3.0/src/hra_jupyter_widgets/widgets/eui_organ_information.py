from traitlets import Enum, List, Unicode

from ..trait_types import Attribute, Event
from ._stylesheets import Font, Material
from .hra_app import HraAppWidget

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ccf-organ-info/"
_DEFAULT_DATA_SOURCES = ["https://purl.humanatlas.io/collection/ds-graphs"]
_DEFAULT_REMOTE_API_ENDPOINT = "https://apps.humanatlas.io/api"


class EuiOrganInformation(HraAppWidget):
    """Displays the HRA EUI organ information application."""

    _tag_name = "ccf-organ-info"
    _scripts = ["https://cdn.humanatlas.io/ui/ccf-organ-info/wc.js"]
    _styles = [
        Font.Inter,
        Material.Icons,
        "https://cdn.humanatlas.io/ui/ccf-organ-info/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF))

    organ_iri = Attribute(Unicode(), required=True, help="Organ to display.")
    sex = Attribute(
        Enum(["Female", "Male"], default_value=None, allow_none=True),
        help="Female or male model when applicable.",
    )
    side = Attribute(
        Enum(["Left", "Right"], default_value=None, allow_none=True),
        help="Left or right organ when applicable.",
    )
    data_sources = Attribute(
        List(Unicode(), default_value=_DEFAULT_DATA_SOURCES),
        help="List of data source urls.",
    )
    highlight_providers = Attribute(
        List(Unicode(), default_value=[]), help="Highlight."
    )
    token = Attribute(Unicode(None, allow_none=True), help="Api token.")
    remote_api_endpoint = Attribute(
        Unicode(_DEFAULT_REMOTE_API_ENDPOINT), help="Api endpoint url."
    )
    donor_label = Attribute(Unicode(None, allow_none=True), help="Label of the donor.")
    rui_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the RUI application."
    )
    eui_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the RUI application."
    )
    asctb_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the ASCT+B application."
    )
    hra_portal_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the HRA portal."
    )
    online_course_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the online course."
    )
    paper_url = Attribute(
        Unicode(None, allow_none=True), help="Url to the associated paper."
    )

    on_sex_change = Event(
        event_name="sexChange",
        help="Event emitted when the user changes between female and male models.",
    )
    on_side_change = Event(
        event_name="sideChange",
        help="Event emitted when the user changes between left and right version of the model.",
    )
    on_node_click = Event(
        event_name="nodeClicked",
        help="Event emitted when the user clicks on a node in the model.",
    )
