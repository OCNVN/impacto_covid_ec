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
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Berries"],
    "Amount": [4, 1, 2, 2],
})

# Create the figure using plotly.graph_objects
fig = go.Figure(data=[
    go.Bar(name='Fruits', x=df['Fruit'], y=df['Amount'])
])

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    
    dcc.Graph(
        id='example-map',
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
        figure=px.choropleth(
            geojson=geojson,
            # locations=["780006B67819952919353"], # This should be a list of locations in your GeoJSON
            color=[0], # This should be a list of values for color
            color_continuous_scale="Viridis",
            range_color=(0, 12),
            labels={'color':'Color'}
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)