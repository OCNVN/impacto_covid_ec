from enum import Enum

class Periodicity(Enum):
    MONTHLY = "Mensual"
    WEEKLY = "Semanal"
    ALL = "Todos"

class Provinces(Enum):
    ZAMORA_CHINCHIPE = "Zamora Chinchipe"
    BOLIVAR = "Bolívar"
    TUNGURAHUA = "Tungurahua"
    PICHINCHA = "Pichincha"
    SUCUMBIOS = "Sucumbíos"
    ESMERALDAS = "Esmeraldas"
    MANABI = "Manabí"
    CARCHI = "Carchi"
    EL_ORO = "El Oro"
    ORELLANA = "Orellana"
    GUAYAS = "Guayas"
    IMBABURA = "Imbabura"
    SANTA_ELENA = "Santa Elena"
    OTRO = "Otro"
    CHIMBORAZO = "Chimborazo"
    LOS_RIOS = "Los Ríos"
    PASTAZA = "Pastaza"
    GALAPAGOS = "Galápagos"
    MORONA_SANTIAGO = "Morona Santiago"
    NAPO = "Napo"
    CANAR = "Cañar"
    LOJA = "Loja"
    STO_DOMINGO_TSACHILAS = "Sto. Domingo Tsáchilas"
    AZUAY = "Azuay"
    COTOPAXI = "Cotopaxi"
    ALL_PROVINCES = "Todas las provincias"

class Metrics(Enum):
    ALL_CAUSES_DEATHS = 'Muertes por todas las causas'
    COVID_DEATHS = 'Muertes causadas por COVID-19'
    COVID_POSITIVE_CASES = 'Casos positivos confirmados de COVID-19'
    VACCINES_DOSSES = 'Dosís de vacunas aplicadas'

class MetricsAndPeriodicity(Enum):
    ALL_CAUSES_MONTHLY_DEATHS = 'all-causes-monthly-deaths'
    ALL_CAUSES_WEEKLY_DEATHS = 'all-causes-weekly-deaths'
    COVID_MONTHLY_DEATHS = 'covid-monthly-deaths'
    COVID_WEEKLY_DEATHS = 'covid-weekly-deaths'
    COVID_TEST_MONTHLY_POSITIVE = 'covid-test-monthly-positive'
    COVID_TEST_WEEKLY_POSITIVE = 'covid-test-weekly-positive'
    VACCINES_MONTHLY_DOSSES = 'vaccines-monthly-dosses'
    VACCINES_WEEKLY_DOSSES = 'vaccines-weekly-dosses'

METRICS_CONFIG = {
    MetricsAndPeriodicity.ALL_CAUSES_MONTHLY_DEATHS.value: {'label': 'Defunciones mensuales', 'periodicity': Periodicity.MONTHLY},
    MetricsAndPeriodicity.ALL_CAUSES_WEEKLY_DEATHS.value: {'label': 'Defunciones semanales', 'periodicity': Periodicity.WEEKLY},
    MetricsAndPeriodicity.COVID_MONTHLY_DEATHS.value: {'label': 'Muertes reportadas mensuales', 'periodicity': Periodicity.MONTHLY},
    MetricsAndPeriodicity.COVID_WEEKLY_DEATHS.value: {'label': 'Muertes reportadas semanales', 'periodicity': Periodicity.WEEKLY},
    MetricsAndPeriodicity.COVID_TEST_MONTHLY_POSITIVE.value: {'label': 'Casos positivos confirmados mensuales', 'periodicity': Periodicity.MONTHLY},
    MetricsAndPeriodicity.COVID_TEST_WEEKLY_POSITIVE.value: {'label': 'Casos positivos confirmados semanales', 'periodicity': Periodicity.WEEKLY},
    MetricsAndPeriodicity.VACCINES_MONTHLY_DOSSES.value: {'label': 'Vacunometro mensual', 'periodicity': Periodicity.MONTHLY},
    MetricsAndPeriodicity.VACCINES_WEEKLY_DOSSES.value: {'label': 'Vacunometro semanal', 'periodicity': Periodicity.WEEKLY},
}
