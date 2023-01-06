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
    - As this is a *not* large scale process, I've used a simple mechanism to keep track of the already processed files. As you can see in the module, the function **s3_load** puts the raw file in a s3-bucket-name/dataset-name/*not_processed*/ location.
    - Once the data of a file has been processed (i.e. loaded into the database), we use the function **move_s3_file** which moves the file to s3-bucket-name/dataset-name/*processed*/
- **src**: All transformation/processing scripts that would be referenced by the Airflow dags come here.
    Ideally we would keep the following structure to keep the repo clean:

    src
    |---Dataset_1
    |   |- dag_task_1
    |   |- dag_task_2
    |   |- dag_task_3
    |
    |---Dataset_2
   ...  |- dag_task_1
        |- dag_task_2
        |- ...
        |- dag_task_n
