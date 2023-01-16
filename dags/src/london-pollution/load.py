#Importing libraries
import json
import sys
import psycopg2

#Appending directory with the module
sys.path.append('/opt/airflow/dags/')


#Importing modeule
from modules.s3LoadTransform import getSecrets, list_s3_files, move_s3_file, call_s3_file

#Defining Vars
secret_name = "secrets_test"
region_name = "eu-west-2"

bucket = 'adriano-portfolio-data-lake-euwest2'
dataset = 'london-pollution'

#Calling Secrets
secrets = getSecrets()

#Database Connection
conn = psycopg2.connect(
    host=secrets.secrets['warehouseHost'],
    database=secrets.secrets['databaseName'],
    user=secrets.secrets['postgresUser'],
    password=secrets.secrets['postgresPassword'])


#Calling the file in the bucket
file_name= list_s3_files(dataset, bucket, secrets)[-1]
file_data = call_s3_file(bucket, file_name, secrets)

#Cleaning the raw file for just the data we need
data = {
    'timestamp':file_data['current']['last_updated'],
    'location': file_data['location']['name'],
    'country': file_data['location']['country'],
    'temp_c':file_data['current']['temp_c'],
    'humidity':file_data['current']['humidity'],
    'co':file_data['current']['air_quality']['co'],
    'no2':file_data['current']['air_quality']['no2'],
    'o3':file_data['current']['air_quality']['o3'],
    'so2':file_data['current']['air_quality']['so2'],
    'pm2_5':file_data['current']['air_quality']['pm2_5'],
    'pm10':file_data['current']['air_quality']['pm10'],
    'us_epa_index':file_data['current']['air_quality']['us-epa-index'],
    'gb_defra_index':file_data['current']['air_quality']['gb-defra-index'],
}


try:
    with conn.cursor() as cur:
        query_sql = """ insert into staging.london_pollution (timestamp, location, country, temp_c, humidity, co, no2, o3, so2, pm2_5, pm10, us_epa_index, gb_defra_index)
        select timestamp, location, country, temp_c, humidity, co, no2, o3, so2, pm2_5, pm10, us_epa_index, gb_defra_index 
        from json_populate_record(NULL::staging.london_pollution, %s) """
        cur.execute(query_sql, (json.dumps(data),))

    move_s3_file(bucket, dataset, file_name, secrets)

    conn.commit()
    print('Data loaded to Postgres succesfully')
except Exception as e:
    print(f'Failed to load data to Postgres: \n {e}')
