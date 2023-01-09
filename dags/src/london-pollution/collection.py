#Importing libraries
import requests
import json
import sys

#Appending directory with the module
sys.path.append('/opt/airflow/dags/')

#Importing modeule + calling secrets
from modules.s3LoadTransform import getSecrets, s3_load
secret_name = "secrets_test"
region_name = "eu-west-2"
secrets = getSecrets(secret_name, region_name)

bucket_name = 'adriano-portfolio-data-lake-euwest2'

print(secrets)

# #Calling API
# api_link = 'https://api.tfl.gov.uk/AirQuality/'
# response = requests.get(api_link)
# json_text = response.json()

# #Dumping response to json
# json_string = json.dumps(json_text)

# #Loading json to S3
# s3_load('london-pollution', json_string, bucket_name, secrets)
