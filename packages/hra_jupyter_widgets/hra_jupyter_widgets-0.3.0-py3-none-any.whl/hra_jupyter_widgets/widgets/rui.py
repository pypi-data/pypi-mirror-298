from traitlets import Bool, Dict, Enum, List, Unicode

from ..trait_types import Attribute, Event
from ._stylesheets import Font, Material
from .hra_app import HraAppIframeWidget

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ccf-rui/"
_DEFAULT_THEME = "hubmap"


class Rui(HraAppIframeWidget):
    """Displays the HRA RUI application."""

    _tag_name = "ccf-rui"
    _scripts = ["https://cdn.humanatlas.io/ui/ccf-rui/wc.js"]
    _styles = [
        Font.Inter,
        Material.Icons,
        "https://cdn.humanatlas.io/ui/ccf-rui/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF, read_only=True))
    _skip_unsaved_changes_confirmation = Attribute(Bool(True, read_only=True))
    # TODO: _logo_tooltip - Maybe set to empty string

    use_download = Attribute(Bool(False), help="Whether to download registrations.")
    reference_data = Attribute(
        Unicode(None, allow_none=True), help="Url to reference data."
    )
    user = Attribute(
        Dict(default_value=None, allow_none=True), help="Preselected user."
    )
    organ = Attribute(
        Dict(default_value=None, allow_none=True), help="Preselected organ."
    )
    edit_registration = Attribute(
        Dict(default_value=None, allow_none=True), help="Previous registrations."
    )
    theme = Attribute(Unicode(_DEFAULT_THEME), help="Application theme.")
    header = Attribute(Bool(False), help="Whether to show the header bar.")
    home_url = Attribute(Unicode(None, allow_none=True), help="Url of the home button.")
    organ_options = Attribute(
        List(Unicode(), default_value=None, allow_none=True), help="Organ options."
    )
    collisions_endpoint = Attribute(
        Unicode(None, allow_none=True), help="Endpoint for collision queries."
    )
    view = Attribute(
        Enum(["register", "3d"], default_value=None, allow_none=True), help="View mode."
    )
    view_side = Attribute(
        Enum(
            ["left", "right", "anterior", "posterior"],
            default_value=None,
            allow_none=True,
        ),
        help="View side.",
    )

    # TODO: register - Turn into an output in ccf-rui
    on_registration = Event(event_name="register")
    # TODO: cancelRegistration - Turn into an output in ccf-rui
    on_cancel_registration = Event(event_name="cancelRegistration")
