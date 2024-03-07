import functools
import json
import operator
import warnings
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union
import folium
import numpy as np
import requests
from branca.colormap import ColorMap, LinearColormap, StepColormap
from branca.element import Element, Figure, Html, IFrame, JavascriptLink, MacroElement
from branca.utilities import color_brewer
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.folium import Map
from folium.map import FeatureGroup, Icon, Layer, Marker, Popup, Tooltip
from folium.utilities import (
    TypeJsonValue,
    TypeLine,
    TypePathOptions,
    _parse_size,
    camelize,
    escape_backticks,
    get_bounds,
    get_obj_in_upper_tree,
    image_to_url,
    javascript_identifier_path_to_array_notation,
    none_max,
    none_min,
    parse_options,
    validate_locations,
)
from folium.vector_layers import Circle, CircleMarker, PolyLine, path_options


class ClickForOneMarker(folium.ClickForMarker):
    """
    Description of the tool
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var new_mark = L.marker();
        function newMarker(e){
        new_mark.setLatLng(e.latlng).addTo({{this._parent.get_name()}});
        new_mark.dragging.enable();
        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
        var lat = e.latlng.lat.toFixed(4),
        lng = e.latlng.lng.toFixed(4);
        new_mark.bindPopup("<a href=https://www.google.com/maps?layer=c&cbll=" + lat + "," + lng + " target=blank >Google Street View</a>");
        parent.document.getElementById("latitude").value = lat;
        parent.document.getElementById("longitude").value =lng;
        };
        {{this._parent.get_name()}}.on('click', newMarker);
        {% endmacro %}
        """) # noqa

    def __init__(self, popup=None):
        super(ClickForOneMarker, self).__init__(popup)
        self._name = 'ClickForOneMarker'


class ClickForLatLng(MacroElement):
    """
    When one clicks on a Map that contains a ClickForLatLng,
    the coordinates of the pointer's position are copied to clipboard.

    Parameters
    ==========
    format_str : str, default 'lat + "," + lng'
        The javascript string used to format the text copied to clipboard.
        eg:
        format_str = 'lat + "," + lng'              >> 46.558860,3.397397
        format_str = '"[" + lat + "," + lng + "]"'  >> [46.558860,3.397397]
    alert : bool, default True
        Whether there should be an alert when something has been copied to clipboard.
    """

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                function getLatLng(e){
                    var lat = e.latlng.lat.toFixed(6),
                        lng = e.latlng.lng.toFixed(6);
                    var txt = {{this.format_str}};
                    navigator.clipboard.writeText(txt);
                    {% if this.alert %}alert("Copied to clipboard : \\n    " + txt);{% endif %}
                    };
                {{this._parent.get_name()}}.on('click', getLatLng);
            {% endmacro %}
            """
    )  # noqa

    def __init__(self, format_str: Optional[str] = None, alert: bool = True):
        super().__init__()
        self._name = "ClickForLatLng"
        self.format_str = format_str or 'lat + "," + lng'
        self.alert = alert

# click_for_marker = ClickForOneMarker()

# map.add_child(click_for_marker)