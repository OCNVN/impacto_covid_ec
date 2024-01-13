import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Load GeoJSON file
with open("./map/geoBoundaries-ECU-ADM1.geojson") as f:
    geojson = json.load(f)
    
# Print properties of each feature
for feature in geojson['features']:
    print(feature['properties'])

# Prepare some data
# df = pd.DataFrame({
#     "Fruit": ["Azuay", "Guayas", "Chimborazo", "Galápagos"],
#     "Amount": [4, 1, 2, 2],
# })

df = pd.read_csv('./data/defunciones_semanal.csv')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-map',
        config={'displayModeBar': False},
        # figure=go.Figure(data=go.Choropleth(
        #     geojson=geojson,
        #     locations=["780006B67819952919353"], # This should be a list of locations in your GeoJSON
        #     z=[0], # This should be a list of values for color
        #     colorscale="Viridis",
        #     zmin=0,
        #     zmax=12,
        #     marker_line_width=0,
        #     showscale=False
        # ))
        # figure=px.choropleth(
        #     geojson=geojson,
        #     # locations=["780006B67819952919353"], # This should be a list of locations in your GeoJSON
        #     color=[0], # This should be a list of values for color
        #     color_continuous_scale="Viridis",
        #     range_color=(0, 12),
        #     labels={'color':'Color'}
        # )
        figure=px.choropleth_mapbox(df,
            geojson=geojson,
            locations="provincia", # This should be a list of locations in your GeoJSON
            featureidkey="properties.shapeName",
            color="semana", # This should be a column in your DataFrame
            color_continuous_scale="Viridis",
            range_color=(0, 12),
            mapbox_style="carto-darkmatter",
            zoom=5,
            center = {"lat": -1.8312, "lon": -78.1834},
            opacity=1,
            labels={'semana':'Semana'},
            
        )
    ),
    html.Pre(id='console-output')
])

@app.callback(dash.dependencies.Output('console-output', 'children'), [dash.dependencies.Input('example-map', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)