import dash
from dash import dcc
from dash import html
from dash import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import json
from constants import Provinces, Metrics, Periodicity
from utils import (
    get_df_by_metric_periodicity,
    get_axis_to_dataframe_column_names,
    get_timeline_slider_params,
    get_filtered_dataframe,
    get_histogram_figure)

# Load GeoJSON file
with open("./map/geoBoundaries-ECU-ADM1.geojson") as f:
    geojson = json.load(f)

# Print properties of each feature
# for feature in geojson['features']:
#     print(feature['properties'])

# Selected values
selected_metric = Metrics.COVID_TEST_POSITIVE.value
selected_province = Provinces.AZUAY.value
selected_periodicity = Periodicity.ALL.value

# Initial values
initial_df = get_df_by_metric_periodicity(selected_metric, selected_periodicity)
initial_x_axis_column_name, initial_y_axis_column_name = get_axis_to_dataframe_column_names(selected_metric, selected_periodicity)
initial_figure = get_histogram_figure(initial_df, initial_x_axis_column_name, initial_y_axis_column_name)
initial_marks, initial_min, initial_max = get_timeline_slider_params(initial_df, initial_x_axis_column_name)

# Dropdowns
metricDropdown = dcc.Dropdown(
    id='metrics-dropdown',
    options=[{'value': member.value, 'label': member.value} for member in Metrics.__members__.values()],
    value=selected_metric
)
provincesDropdown = dcc.Dropdown(
    id='provinces-dropdown',
    options=[{'value': Provinces.ALL_PROVINCES.value, 'label': Provinces.ALL_PROVINCES.value}] +
            sorted([{'value': member.value, 'label': member.value} for member in Provinces.__members__.values() if
                    member != Provinces.ALL_PROVINCES], key=lambda x: x['value']),
    value=selected_province
)
periodicityDropdown = dcc.Dropdown(
    id='periodicity-dropdown',
    options=[{'value': member.value, 'label': member.value} for member in Periodicity.__members__.values()],
    value=selected_periodicity
)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    dcc.Store(id='metric-selected-store', data=selected_metric),
    dcc.Store(id='province-selected-store', data=selected_province),
    dcc.Store(id='periodicity-selected-store', data=selected_periodicity),

    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    metricDropdown,
    provincesDropdown,
    periodicityDropdown,
    dcc.Graph(
        id='provinces-map',
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
        figure=px.choropleth_mapbox(initial_df,
                                    geojson=geojson,
                                    locations="provincia",  # This should be a list of locations in your GeoJSON
                                    featureidkey="properties.shapeName",
                                    color="semana",  # This should be a column in your DataFrame
                                    color_continuous_scale=None,
                                    range_color=(0, 12),
                                    mapbox_style="carto-darkmatter",
                                    zoom=5,
                                    center={"lat": -1.8312, "lon": -78.1834},
                                    opacity=1,
                                    labels={'semana': 'Semana'},

                                    ),
    ),
    html.Pre(id='console-output'),
    html.Pre(id='metric-output'),
    html.Pre(id='console-output-slider'),
    dcc.Graph(
        id='histogram-1',
        config={'displayModeBar': False},
        figure=initial_figure
    ),
    dcc.RangeSlider(
        id='timeline-slider',
        step=None,
        marks=initial_marks,
        min=initial_min,
        max=initial_max,
        value=[initial_min, initial_max]
    ),
])



# @app.callback(Output('console-output', 'children'), [Input('provinces-map', 'clickData')])
# def on_province_selected(clickData):
#     return json.dumps(clickData, indent=2)


# Callback to update the store whenever the selection changes
@app.callback(Output('metric-selected-store', 'data'), [Input('metrics-dropdown', 'value')])
def on_metric_selected(selected_value):
    return selected_value
@app.callback(Output('province-selected-store', 'data'), [Input('provinces-dropdown', 'value')])
def on_province_selected(selected_value):
    return selected_value
@app.callback(Output('periodicity-selected-store', 'data'), [Input('periodicity-dropdown', 'value')])
def on_periodicity_selected(selected_value):
    return selected_value
@app.callback(
    Output('console-output-slider', 'children'),
    Input('timeline-slider', 'value')
)
def on_timeline_range_change(value):
    return 'Range slider value: {}'.format(value)


@app.callback([Output('histogram-1', 'figure'),
               Output('timeline-slider', 'marks'),
               Output('timeline-slider', 'min'),
               Output('timeline-slider', 'max'),
               Output('timeline-slider', 'value')],
              [Input('metric-selected-store', 'data'),
               Input('province-selected-store', 'data'),
               Input('periodicity-selected-store', 'data')])
def update_output(metric_selected, province_selected, periodicity_selected):
    df = get_df_by_metric_periodicity(metric_selected, periodicity_selected)
    df_filtered = get_filtered_dataframe(df, province_selected)
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(metric_selected, periodicity_selected)
    figure = get_histogram_figure(df_filtered, x_axis_column_name, y_axis_column_name)
    marks, min, max = get_timeline_slider_params(df_filtered, x_axis_column_name)
    return figure, marks, min, max, [min, max],



if __name__ == '__main__':
    app.run_server(debug=True)
