import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

secret_name = "secrets_test"
region_name = "eu-west-2"


class getSecrets:
    def __init__(self, secret_name, region_name):
        self.secret_name = secret_name
        self.region_name = region_name
        self.secrets = self.get_secret()

    def get_secret(self):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']

        return json.loads(secret)


def s3_load(bucket, dataset_name, json_string):

    secrets = getSecrets(secret_name, region_name)
    access_key = secrets.secrets['accessKey']
    secret_access_key = secrets.secrets['secretAccessKey']

    utcs_now = datetime.utcnow().strftime('%Y%m%d%H%M')
    client = boto3.client('s3',
                    aws_access_key_id = access_key,
                    aws_secret_access_key = secret_access_key)
    key = f"{dataset_name}/not_processed/{dataset_name}_{utcs_now}.json"
    client.put_object(Body = json_string, 
                Bucket = bucket, 
                Key = key)
    print(f"File {key} has been uploaded to S3")


def list_s3_files(bucket, dataset_name):

    secrets = getSecrets(secret_name, region_name)
    access_key = secrets.secrets['accessKey']
    secret_access_key = secrets.secrets['secretAccessKey']

    s3 = boto3.resource('s3',
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_access_key)
    files = []
    my_bucket = s3.Bucket(bucket)
    for object_name in my_bucket.objects.filter(Prefix=f"{dataset_name}/not_processed/"):
        files.append(object_name.key)
    
    return files


def move_s3_file(bucket, dataset_name, object_name):

    secrets = getSecrets(secret_name, region_name)
    access_key = secrets.secrets['accessKey']
    secret_access_key = secrets.secrets['secretAccessKey']

    s3 = boto3.resource('s3',
                aws_access_key_id = access_key,
                aws_secret_access_key = secret_access_key)
    file = object_name.split('/')[-1]

    old_key = f"{dataset_name}/not_processed/{file}"
    new_key = f"{dataset_name}/processed/{file}"

    old_name = f"{bucket}/{old_key}"

    s3.Object(bucket, new_key).copy_from(CopySource=old_name)
    s3.Object(bucket, old_key).delete()
    print(f"File {old_name} has been moved to the processed directory (new file key: {bucket}/{new_key})")


