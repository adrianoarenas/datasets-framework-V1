Please refer first to [data-pipeline-framework-V1](https://github.com/adrianoarenas/data-pipeline-framework-V1) for the architecture deployment repo.

<br/><br/>

# Adding, updating and deleting datasets in the ETL framework
---

All dags and transformations scripts (dbt or python) are deployed to the EC2 instance created in [data-pipeline-framework-V1](https://github.com/adrianoarenas/data-pipeline-framework-V1) via rsync.

The deployment is done via Github Actions with the [ssh deploy](https://github.com/marketplace/actions/ssh-deploy) workflow. (See the yml file [here](https://github.com/adrianoarenas/datasets-framework-V1/blob/main/.github/workflows/push-to-ec2.yml))

To set up the Github Actions deployment, 2 secrets must be added to Github Secrets:
- EC2_SSH_KEY: ssh key to connect to the ec2 instance.
- EC2_HOST: public host of the EC2 instance.

Ideally all changes will be created in a feature branch and a PR to **main** will trigger the action and sync the repo with the EC2 instance.


The setup of this repo is the following:
- **dags**: All Airflow dags will go in this folder, Airflow is setup to read the dags from here.
- **modules**: For the sake of keeping this repo clean, any modules created come here. For now I created a module to standardize the load of the raw files to S3 as well to process the raw files into the DB.
- **src**: All transformation/processing scripts that would be referenced by the Airflow dags come here.
    Ideally we would keep the following structure to keep the repo clean:

```
src 
│
└───Dataset_1
│   │── dag_task_1.py
│   │── dag_task_2.py
│   │── dag_task_3.py
│   
│   
└───Dataset_2
│   │── dag_task_1.py
│   │── dag_task_2.py
│   │   ...
│   │── dag_task_n.py
│
...
```

<br/><br/>

As this is a *not* large scale process, I've used a simple mechanism to keep track of the already processed files:
1. As you can see in the module, the function **s3_load** puts the raw file in a s3-bucket-name/dataset-name/*not_processed*/ location.
2. Once the data of a file has been processed (i.e. loaded into the database), we use the function **move_s3_file** which moves the file to s3-bucket-name/dataset-name/*processed*/

This way we know that on the next run of the dag, the processing script will not re-process an already processed file as we just read from the *not_processed* location.

```
s3-bucket 
│
└───dataset-1-name
│   │── not_processed
│   │   │── raw-file.json
│   │   │── raw-file.json
│   │
│   │── processed
│   │── raw-file.json
│   │── raw-file.json
│   │── ...
│   │── raw-file.json
│   
│   
└───dataset-2-name
│   │── not_processed
│   │   │── raw-file.json
│   │
│   │── processed
│   │── raw-file.json
│   │── raw-file.json
│   │── ...
│   │── raw-file.json
...
```

<br/><br/>

to do:
Finish commenting/documenting the functions in the s3LoadTransform.py module