from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import PopulationApp as App

import json
from pathlib import Path
import requests


@controller(name='home', app_workspace=True)
class PopulationMap(MapLayout):
    app = App
    base_template = 'population_app/base.html'
    map_title = 'Population Tracker'
    show_properties_popup = True
    plot_slide_sheet = True

    basemaps = ['OpenStreetMap', 'ESRI']
    default_map_extent = [-73.81, -57.49, 91.30, 73.71]

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """ Override the compose_layers method to add GeoJSON layers to the map. """
        # Load GeoJSON data
        geojson_file = Path(app_workspace.path) / 'population_app' / 'data' / 'country_borders.geojson'

        with open(geojson_file) as f:
            geojson_data = json.load(f)

        countries_layer = self.build_geojson_layer(
            geojson=geojson_data,
            layer_name='countries',
            layer_title='Countries',
            layer_variable='countries_layer_var',
            visible=True,
            selectable=True,
            plottable=True,
            excluded_properties=['ISO_A3', 'ISO_A2'],
            popup_title='Country Info'
        )

        layer_groups = [
            self.build_layer_group(
                id='geojson_layers',
                display_name='Countries',
                layer_control='checkbox',
                layers=[
                    countries_layer
                ]
            )
        ]

        return layer_groups
    
    def get_plot_for_layer_feature(request, layer_name, feature_id ,layer_data, feature_props, *args, **kwargs):
        """ Override the get_plot_for_layer_feature method to add a plot to the map. """
        # Define parameters 
        country_code = args[0].get('ISO_A3')
        country_name = args[0].get('ADMIN')
        indicator = 'SP.POP.TOTL'
        start_year = 2000
        end_year = 2023
        url = f'https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}'

        response = requests.get(url, params={'date': f'{start_year}:{end_year}', 'format': 'json'})

        if response.status_code == 200:
            data = response.json()
            years = []
            population_values = []
            if len(data) > 1:
                for entry in data[1]:
                    years.append(entry['date'])
                    population_values.append(entry['value'])
                    
            else:
                print("No data available for that range of years")
                return None, None, None
        else:
            print("Couldn't retrieve data")
            return None, None, None
        
        layout = {
            'yaxis': {
                'title': 'Population',
            },
            'xaxis': {
                'title': 'Year',
            },
        }
        data = [
                {
                    'name': 'Population',
                    'mode': 'lines',
                    'x': years,
                    'y': population_values,
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]
        

        return f'Population of {country_name} from {start_year} to {end_year}', data, layout
    