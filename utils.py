import folium
import json
import geopandas
import numpy as np
import pandas as pd
import psycopg2

from folium.plugins import MarkerCluster
from geopandas import tools
from shapely.geometry import Point




class MarkerClusterScript(MarkerCluster):
    def __init__(self, data, callback, popup=None):
        from jinja2 import Template
        super(MarkerClusterScript, self).__init__([])
        self._name = 'Script'
        self._data = data
        self._popup = popup
        if callable(callback):
            from flexx.pyscript import py2js
            self._callback = py2js(callback, new_name="callback")
        else:
            self._callback = "var callback = {};".format(_callback)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            (function(){
                var data = {{this._data}};
                var map = {{this._parent.get_name()}};
                var cluster = L.markerClusterGroup();
                {{this._callback}}

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row, popup='"""+ popup +"""');
                    marker.addTo(cluster);
                }

                cluster.addTo(map);
            })();
            {% endmacro %}
                        """)
        
def create_marker(row, popup=None):
    """Returns a L.marker object"""
    icon = L.AwesomeMarkers.icon({icon:'flag',markerColor: 'red'})    
    marker = L.marker(L.LatLng(row.latitude, row.longitude))
    marker.bindPopup(str(row[popup]))
    marker.setIcon(icon)
    return marker