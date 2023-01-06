# Adding, updating and deleting datasets in the ETL framework
---

All dags and transformations scripts (dbt or python) are deployed to the EC2 instance created in [data-pipeline-framework-V1](https://github.com/adrianoarenas/data-pipeline-framework-V1) via rsync.

The deployment is done via Github Actions with the [ssh deploy](https://github.com/marketplace/actions/ssh-deploy) workflow. (See the yml file [here](https://github.com/adrianoarenas/datasets-framework-V1/blob/main/.github/workflows/push-to-ec2.yml))

To set up the Github Actions deployment, 2 secrets must be added to Github Secrets:
- EC2_SSH_KEY: ssh key to connect to the ec2 instance.
- EC2_HOST: public host of the EC2 instance.

Ideally all changes will be created in a feature branch and a PR to **main** will trigger the action and sync the repo with the EC2 instance.