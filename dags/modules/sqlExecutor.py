#Importing Libraries
import psycopg2
import sys

from s3LoadTransform import getSecrets

#Defining Vars
secret_name = "secrets_test"
region_name = "eu-west-2"

#Calling Secrets
secrets = getSecrets(secret_name, region_name)


#Sys is going to be used to manually input the name of the SQL file to be run in the database

#Database Connection
conn = psycopg2.connect(
    host=secrets.secrets['warehouseHost'],
    database=secrets.secrets['databaseName'],
    user=secrets.secrets['postgresUser'],
    password=secrets.secrets['postgresPassword'])


try:
    with conn.cursor() as cur:
        cur.execute(open(sys.argv[1], "r").read())
    print(f"SQL script {sys.argv[1]} executed")
except Exception as e:
    print(f'Failed to execute {sys.argv[1]} \n')
    print(e)
    print("Rolling back")
    with conn.cursor() as cur:
        cur.execute("rollback;")