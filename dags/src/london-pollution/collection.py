#Importing libraries
import requests
import json
import sys

#Appending directory with the module
sys.path.append('/opt/airflow/dags/')

#Importing modeule
from modules.s3LoadTransform import getSecrets, s3_load

#Defining Vars
secret_name = "secrets_test"
region_name = "eu-west-2"

bucket = 'adriano-portfolio-data-lake-euwest2'
dataset = 'london-pollution'

#Calling Secrets
secrets = getSecrets(secret_name, region_name)

#API vars
api_key = secrets.secrets['londonPollutionApiKey']
location = 'london'
air_quality_data = 'yes'

api_link = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi={air_quality_data}'

def loading_data_to_s3():
    #Calling API
    response = requests.get(api_link)
    json_text = response.json()
    #Dumping response to json
    json_string = json.dumps(json_text)
    #Loading json to S3
    s3_load(dataset, json_string, bucket, secrets)

try:
    loading_data_to_s3()
except Exception as e:
    print(f'Failed to load json to S3: \n {e}')