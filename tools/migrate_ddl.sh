#!/bin/bash

python -m migrations.defunciones_mensual_migration_ddl
python -m migrations.defunciones_semanal_migration_ddl
python -m migrations.muertes_covid_mensual_migration_ddl
python -m migrations.muertes_covid_semanal_migration_ddl
python -m migrations.positivas_mensual_migration_ddl
python -m migrations.positivas_semanal_migration_ddl
python -m migrations.vacunometro_mensual_migration_ddl
python -m migrations.vacunometro_semanal_migration_ddl
