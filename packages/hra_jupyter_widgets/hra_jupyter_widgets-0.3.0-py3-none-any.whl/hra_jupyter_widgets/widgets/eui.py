from traitlets import Bool, Dict, List, Unicode

from ..trait_types import Attribute
from ._stylesheets import Font, Material
from .hra_app import HraAppIframeWidget

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ccf-eui/"
_DEFAULT_DATA_SOURCES = ["https://purl.humanatlas.io/collection/ds-graphs"]
_DEFAULT_REMOTE_API_ENDPOINT = "https://apps.humanatlas.io/api"
_DEFAULT_THEME = "hubmap"


class Eui(HraAppIframeWidget):
    """Displays the HRA EUI application."""

    _tag_name = "ccf-eui"
    _scripts = ["https://cdn.humanatlas.io/ui/ccf-eui/wc.js"]
    _styles = [
        Font.Inter,
        Material.Icons,
        "https://cdn.humanatlas.io/ui/ccf-eui/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF, read_only=True))
    _home_url = Attribute(Unicode("", read_only=True))
    # TODO: _logo_tooltip - Maybe set to empty string
    _login_disabled = Attribute(Bool(True, read_only=True))

    data_sources = Attribute(
        List(Unicode(), default_value=_DEFAULT_DATA_SOURCES), help="Data source urls."
    )
    selected_organs = Attribute(List(Unicode()), help="List of selected organs.")
    token = Attribute(Unicode(None, allow_none=True), help="Api token.")
    remote_api_endpoint = Attribute(
        Unicode(_DEFAULT_REMOTE_API_ENDPOINT), help="Api endpoint url."
    )
    theme = Attribute(Unicode(_DEFAULT_THEME), help="Application theme.")
    header = Attribute(Bool(False), help="Whether to display the header bar.")
    filter = Attribute(Dict(default_value=None, allow_none=True), help="Data filter.")
