import dash
from dash import dcc
from dash import html
from dash import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import json
from constants import Provinces, Metrics, Periodicity
from utils import (
    get_df_by_metric_periodicity,
    get_axis_to_dataframe_column_names,
    get_timeline_slider_params,
    get_filtered_dataframe,
    get_histogram_figure,
    get_province_from_choropleth_click_data)

# Load GeoJSON file
with open("./map/geoBoundaries-ECU-ADM1.geojson") as f:
    geojson = json.load(f)

# Selected values
selected_metric = Metrics.COVID_POSITIVE_CASES.value
selected_province = Provinces.AZUAY.value
selected_periodicity = Periodicity.ALL.value

# Initial values
initial_df = get_df_by_metric_periodicity(selected_metric, selected_periodicity)
initial_x_axis_column_name, initial_y_axis_column_name = get_axis_to_dataframe_column_names(selected_metric)

initial_figure = get_histogram_figure(initial_df, initial_x_axis_column_name, initial_y_axis_column_name)
initial_marks, initial_min, initial_max = get_timeline_slider_params(initial_df, initial_x_axis_column_name)

initial_positive_cases_df = get_df_by_metric_periodicity(Metrics.COVID_POSITIVE_CASES.value, Periodicity.ALL.value)
initial_positive_cases_df = get_filtered_dataframe(initial_positive_cases_df, selected_province)
initial_positive_cases_x_axis_column_name, initial_positive_cases_y_axis_column_name = get_axis_to_dataframe_column_names(
    Metrics.COVID_POSITIVE_CASES.value)
initial_positive_cases_figure = get_histogram_figure(initial_positive_cases_df,
                                                     initial_positive_cases_x_axis_column_name,
                                                     initial_positive_cases_y_axis_column_name)

initial_all_deaths_df = get_df_by_metric_periodicity(Metrics.ALL_CAUSES_DEATHS.value, Periodicity.ALL.value)
initial_all_deaths_df = get_filtered_dataframe(initial_all_deaths_df, selected_province)
initial_all_deaths_x_axis_column_name, initial_all_deaths_y_axis_column_name = get_axis_to_dataframe_column_names(
    Metrics.ALL_CAUSES_DEATHS.value)
initial_all_deaths_figure = get_histogram_figure(initial_all_deaths_df,
                                                 initial_all_deaths_x_axis_column_name,
                                                 initial_all_deaths_y_axis_column_name)

initial_covid_deaths_df = get_df_by_metric_periodicity(Metrics.COVID_DEATHS.value, Periodicity.ALL.value)
initial_covid_deaths_df = get_filtered_dataframe(initial_covid_deaths_df, selected_province)
initial_covid_deaths_x_axis_column_name, initial_covid_deaths_y_axis_column_name = get_axis_to_dataframe_column_names(
    Metrics.COVID_DEATHS.value)
initial_covid_deaths_figure = get_histogram_figure(initial_covid_deaths_df,
                                                   initial_covid_deaths_x_axis_column_name,
                                                   initial_covid_deaths_y_axis_column_name)

initial_vaccine_dosses_df = get_df_by_metric_periodicity(Metrics.VACCINES_DOSSES.value, Periodicity.ALL.value)
initial_vaccine_dosses_df = get_filtered_dataframe(initial_vaccine_dosses_df, selected_province)
initial_vaccine_dosses_x_axis_column_name, initial_vaccine_dosses_y_axis_column_name = get_axis_to_dataframe_column_names(
    Metrics.VACCINES_DOSSES.value)
initial_vaccine_dosses_figure = get_histogram_figure(initial_vaccine_dosses_df,
                                                     initial_vaccine_dosses_x_axis_column_name,
                                                     initial_vaccine_dosses_y_axis_column_name)

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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Store(id='metric-selected-store', data=selected_metric),
            dcc.Store(id='province-selected-store', data=selected_province),
            dcc.Store(id='periodicity-selected-store', data=selected_periodicity),
            html.Div(children='Impacto del COVID-19 en el Ecuador', style={'textAlign': 'center', 'fontSize': 30}),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([

        ], width=3),
        dbc.Col([
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
                                            range_color=(initial_min, initial_max),
                                            mapbox_style="carto-darkmatter",
                                            zoom=5,
                                            center={"lat": -1.8312, "lon": -78.1834},
                                            opacity=1,
                                            labels={'semana': 'Semana'},
                                            ).update_layout(margin=dict(l=0, r=0, t=0, b=0)
                                                            # Adjust these values as needed
                                                            ),
            ),
            metricDropdown,
            provincesDropdown,
            periodicityDropdown,
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='vaccine-dosses-graph',
                config={'displayModeBar': False},
                figure=initial_vaccine_dosses_figure.update_layout(height=120)
            ),
            dcc.Graph(
                id='positive-cases-graph',
                config={'displayModeBar': False},
                figure=initial_positive_cases_figure.update_layout(height=120)
            ),
            dcc.Graph(
                id='all-deaths-graph',
                config={'displayModeBar': False},
                figure=initial_all_deaths_figure.update_layout(height=120)
            ),
            dcc.Graph(
                id='covid-deaths-graph',
                config={'displayModeBar': False},
                figure=initial_covid_deaths_figure.update_layout(height=120)
            ),
        ], width=3, style={'height': '100%', 'overflow': 'auto'}),
        html.Pre(id='console-output'),
        html.Pre(id='console-output-map'),
        html.Pre(id='metric-output'),
        dcc.Graph(
            id='histogram-1',
            config={'displayModeBar': False},
            figure=initial_figure
        ),
        html.Pre(id='console-output-slider'),
        dcc.RangeSlider(
            id='timeline-slider',
            step=None,
            marks=initial_marks,
            min=initial_min,
            max=initial_max,
            value=[initial_min, initial_max]
        ),
    ])
], fluid=True)


@app.callback([Output('console-output', 'children'), Output('province-selected-store', 'data')],
              [Input('provinces-map', 'clickData')])
def on_province_selected(clickData):
    province = clickData['points'][0]['location'] if clickData else Provinces.AZUAY.value
    return province, province


# Callback to update the store whenever the selection changes
@app.callback(Output('metric-selected-store', 'data'), [Input('metrics-dropdown', 'value')])
def on_metric_selected(selected_value):
    return selected_value


# @app.callback(Output('province-selected-store', 'data'), [Input('provinces-dropdown', 'value')])
# def on_province_selected(selected_value):
#     return selected_value
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
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(metric_selected)
    figure = get_histogram_figure(df_filtered, x_axis_column_name, y_axis_column_name)
    marks, min, max = get_timeline_slider_params(df_filtered, x_axis_column_name)
    return figure, marks, min, max, [min, max],


@app.callback([Output('vaccine-dosses-graph', 'figure')],
              [[Input('provinces-map', 'clickData')]])
def update_vaccine_dosses_graph(click_data):
    selected_province = get_province_from_choropleth_click_data(click_data)

    df = get_df_by_metric_periodicity(Metrics.VACCINES_DOSSES.value, Periodicity.ALL.value)
    df = get_filtered_dataframe(df, selected_province)
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(Metrics.VACCINES_DOSSES.value)
    figure = get_histogram_figure(df, x_axis_column_name, y_axis_column_name)
    return figure,


@app.callback([Output('positive-cases-graph', 'figure')],
              [[Input('provinces-map', 'clickData')]])
def update_positive_cases_graph(click_data):
    selected_province = get_province_from_choropleth_click_data(click_data)

    df = get_df_by_metric_periodicity(Metrics.COVID_POSITIVE_CASES.value, Periodicity.ALL.value)
    df = get_filtered_dataframe(df, selected_province)
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(Metrics.COVID_POSITIVE_CASES.value)
    figure = get_histogram_figure(df, x_axis_column_name, y_axis_column_name)
    return figure,


@app.callback([Output('all-deaths-graph', 'figure')],
              [[Input('provinces-map', 'clickData')]])
def update_all_deaths_graph(click_data):
    selected_province = get_province_from_choropleth_click_data(click_data)

    df = get_df_by_metric_periodicity(Metrics.ALL_CAUSES_DEATHS.value, Periodicity.ALL.value)
    df = get_filtered_dataframe(df, selected_province)
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(Metrics.ALL_CAUSES_DEATHS.value)
    figure = get_histogram_figure(df, x_axis_column_name, y_axis_column_name)
    return figure,


@app.callback([Output('covid-deaths-graph', 'figure')],
              [[Input('provinces-map', 'clickData')]])
def update_all_deaths_graph(click_data):
    selected_province = get_province_from_choropleth_click_data(click_data)

    df = get_df_by_metric_periodicity(Metrics.COVID_DEATHS.value, Periodicity.ALL.value)
    df = get_filtered_dataframe(df, selected_province)
    x_axis_column_name, y_axis_column_name = get_axis_to_dataframe_column_names(Metrics.COVID_DEATHS.value)
    figure = get_histogram_figure(df, x_axis_column_name, y_axis_column_name)
    return figure,


@app.callback(Output('provinces-map', 'figure'),
              Input('provinces-map', 'clickData'),
              State('provinces-map', 'figure'))
def update_map_with_selected_province(click_data, figure):
    if click_data:
        # Get the clicked location
        clicked_location = click_data['points'][0]['location']

        # Update the color of the clicked location in the DataFrame
        for i in range(len(figure['data'][0]['locations'])):
            if figure['data'][0]['locations'][i] == clicked_location:
                figure['data'][0]['marker']['color'][i] = 'red'  # Change the color to red

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
