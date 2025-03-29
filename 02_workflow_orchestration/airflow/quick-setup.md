# Airflow Setup

## Move GCP credentials to $HOME directory

Currently the keys are under `01_docker_terraform > 1_terraform > keys` and we are required to move to the home directory of the machine

```bash
mv "<location_of_keys>" "$HOME/google_credentials.json" 
```

```bash
## Export to .zshrc
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/google_credentials.json"' >> ~/.zshrc

## Reload file
source ~/.zshrc
```

Finally check if the Google application credentials are present in the local machine `echo $GOOGLE_APPLICATION_CREDENTIALS`


## Set the Airflow user (Mac)

On Linux, the quick-start needs to know your host user-id and needs to have group id set to 0. 
Otherwise the files created in `dags`, `logs` and `plugins` will be created with root user. 
You have to make sure to configure them for the docker-compose:

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

## Check the user Id
cat .env
```

## Import the official docker setup file from the latest

Airflow version: 
```shell
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```
OR 

Use the docker-compose file from notes from a peers [github repo](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/blob/main/2_Workflow-Orchestration-AirFlow/airflow/docker-compose.yaml)

## Ensure Google credentials are being accessed  

Add the following into the `docker-compose.yaml` to ensure google creds are being accessed - 

```yaml

        - GCP_PROJECT_ID=${GCP_PROJECT_ID}
        - GCP_GCS_BUCKET=${GCP_GCS_BUCKET}
        - GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
        - AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT=${AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT}
```

The above variables can be accessed in the `.env` file that should be git ignored. 

## Adding dependencies

Ensure the `requirement.txt` is added to included libraries to assist with GCP integration and parquet file manipulation. 

## Docker-compose

1. Build the image (only first-time, or when there's any change in the `Dockerfile`, takes ~15 mins for the first-time):
     ```shell
     docker-compose build
     ```
   
     or (for legacy versions)
   
     ```shell
     docker build .
     ```

 2. Initialize the Airflow scheduler, DB, and other config
    ```shell
    docker-compose up airflow-init
    ```

 3. Kick up the all the services from the container:
    ```shell
    docker-compose up
    ```

 4. In another terminal, run `docker-compose ps` to see which containers are up & running (there should be 7, matching with the services in your docker-compose file).

 5. Login to Airflow web UI on `localhost:8080` with default creds

 6. Run your DAG on the Web Console.

 7. On finishing your run or to shut down the container/s:
    ```shell
    docker-compose down
    ```

    To stop and delete containers, delete volumes with database data, and download images, run:
    ```
    docker-compose down --volumes --rmi all
    ```

    or
    ```
    docker-compose down --volumes --remove-orphans
    ```