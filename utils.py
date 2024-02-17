import plotly.graph_objects as go
from dataframes.defunciones_mensual_df import get_defunciones_mensual
from dataframes.defunciones_semanal_df import get_defunciones_semanal
from dataframes.positivas_semanal_df import get_positivas_semanal
from dataframes.positivas_mensual_df import get_positivas_mensual
from dataframes.vacunometro_mensual_df import get_vacunometro_mensual
from dataframes.vacunometro_semanal_df import get_vacunometro_semanal
from dataframes.muertes_covid_semanal_df import get_muertes_covid_semanal
from dataframes.muertes_covid_mensual_df import get_muertes_covid_mensual
from constants import Metrics, Periodicity, Provinces

def get_df_by_metric_periodicity(metric, periodicity):
    return {
        (Metrics.COVID_POSITIVE_CASES.value, Periodicity.WEEKLY.value): get_positivas_semanal(),
        (Metrics.COVID_POSITIVE_CASES.value, Periodicity.ALL.value): get_positivas_semanal(),
        (Metrics.COVID_POSITIVE_CASES.value, Periodicity.MONTHLY.value): get_positivas_mensual(),
        (Metrics.COVID_DEATHS.value, Periodicity.WEEKLY.value): get_muertes_covid_semanal(),
        (Metrics.COVID_DEATHS.value, Periodicity.ALL.value): get_muertes_covid_semanal(),
        (Metrics.COVID_DEATHS.value, Periodicity.MONTHLY.value): get_muertes_covid_mensual(),
        (Metrics.ALL_CAUSES_DEATHS.value, Periodicity.WEEKLY.value): get_defunciones_semanal(),
        (Metrics.ALL_CAUSES_DEATHS.value, Periodicity.ALL.value): get_defunciones_semanal(),
        (Metrics.ALL_CAUSES_DEATHS.value, Periodicity.MONTHLY.value): get_defunciones_mensual(),
        (Metrics.VACCINES_DOSSES.value, Periodicity.WEEKLY.value): get_vacunometro_semanal(),
        (Metrics.VACCINES_DOSSES.value, Periodicity.ALL.value): get_vacunometro_semanal(),
        (Metrics.VACCINES_DOSSES.value, Periodicity.MONTHLY.value): get_vacunometro_mensual(),
    }.get((metric, periodicity))

def get_axis_to_dataframe_column_names(metric):
    x_axis_column_name = 'timestamp'
    y_axis_column_name = 'total' if metric == Metrics.ALL_CAUSES_DEATHS.value else 'dosis_total' if metric == Metrics.VACCINES_DOSSES.value else 'nuevas'
    return x_axis_column_name, y_axis_column_name

def get_timeline_slider_params(df, x_axis_column_name):
    min = df[x_axis_column_name].min()
    max = df[x_axis_column_name].max()

    marks = {str(column): str(column) for column in df[x_axis_column_name].unique()}
    return marks, min, max

def get_filtered_dataframe(df, province):
    df_filtered = df.loc[(df['provincia'] == province)]
    return df_filtered

def get_histogram_figure(df, x_axis_column_name, y_axis_column_name):
    bar = go.Scatter(
        x=df[x_axis_column_name],
        y=df[y_axis_column_name],
        mode='lines',
        fill='tozeroy',
        hovertemplate='Total: x = %{x}, y = %{y}<extra></extra>'
    )
    figure = go.Figure(
        data=[bar],
        layout=go.Layout(
            # xaxis={'title': x_axis_column_name},
            yaxis={'title': y_axis_column_name},

            # xaxis={'title': None, 'automargin': True},
            # yaxis={'title': None, 'automargin': True},
            bargap=0.1,
            margin=dict(l=0, r=0, t=0, b=0)  # Adjust these values as needed
        )
    )
    return figure

def get_province_from_choropleth_click_data(click_data):
    if click_data is None:
        return Provinces.AZUAY.value
    return click_data['points'][0]['location']
