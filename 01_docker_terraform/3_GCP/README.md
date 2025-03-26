## Create SSH Directory

- Create an `.ssh` directory on your local machine.  
- Follow this [guide](https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos) to generate an SSH key in your `.ssh` directory.  
- Use the public key to upload it to your Google account.  


## Create a VM instance

- Create an instance in the region you are located in 
- Changed the OS to Ubuntu and allocated 20GB
- (Extra Cost) Change the external IP from `ephemeral` to a `static` external IP to prevent editing the config in the `.ssh` everytime
- Selected an e2-standard-4
- Use the below command to connect to the instance

```bash
ssh -i ~/.ssh/<gcp_privatekey> <username>@<Instance_external_IP>
```

## Creating a config file in the `ssh` directory

Here we are configuring a file to so that we do not have to run the `ssh` command every single time to connect to our instance. 

- Go to your `ssh` directory and create a config file by running `touch config`
- Open the `config` file and insert the following - 

```bash
Host <instance_name>
    HostName <instance_external_ip>
    User xyz
    IdentityFile ~/.ssh/<private-key>
```

Now to connect to the instance, we should navigate to the `.ssh` directory and run `ssh instance_name`. In our case it would be `ssh de-zoomcamp`

## Setting up the VM instance

### Install Docker

1) To install docker in the instance - 
- `sudo apt-get update`
- `sudo apt-get install docker.io`

2) To verify if docker is properly installed, run `docker run hello-world`

3) If the above complains about permissions, we can add docker to the group user to run without `sudo` - follow this [link](https://docs.docker.com/engine/install/linux-postinstall/)

4) Install the lastest docker compose using this [github-link](https://github.com/docker/compose/tags) for `docker-compose-linux-x86_64` in the `bin` folder, create it if it doesn't exist. 

```bash
wget <git_tag_link> -O docker-compose
```

5) Export it to the `.bashrc`

```bash
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Install anaconda in the instance

- Check the google cloud version `glcoud --version`

- Download anaconda in instance
`wget https://repo.anaconda.com/archive/<latest_anaconda_version>`

- Install the downloaded anaconda version
`bash <latest_anaconda_version>`

#### Troubleshooting

Verify to see if python has been installed by running `which python`. If it's not then most likely it's not in the environment variable. 

Add the python installed location to `~/.bashrc`. Can follow the below steps - 

- Run `export PATH=$HOME/anaconda3/bin:$PATH` amd run `which python` to temporarily add the path to the environment. 

- Now if python is found, export it to `~/.bashrc` to persist after a restart of the instance

```bash
echo 'export PATH=$HOME/anaconda3/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

> **Note:** Why is `$HOME` and `:$PATH` added?  
> - `$HOME` is an environment variable that expands to your home directory. Instead of hardcoding `/home/your-username`, using `$HOME` makes the command work for any user.  
> - `:$PATH` ensures that the existing paths are preserved while adding the Anaconda `bin` directory at the beginning. This means the system will prioritize Anaconda's Python over other versions but still allow access to all other commands.  
> - If `:$PATH` were omitted, the system might lose access to essential commands like `ls` and `vim` because they rely on paths in the original `$PATH` variable.

### Set up VSCode to access our instance

Go to extensions and install the plugin - `Remote SSH` by Microsoft. After installing, find the blue icon in the buttom left of your editor to and 'open a remote window'. 

Ideally because we've already created the `config` file earlier, you should find the `hostname` in the prompt. 

#### Cloning this repo in our instance

`git clone https://github.com/vaurnramesh/data_engineering_zoomcamp_2025.git`

### Install terraform in the instance

- Follow this (link)[https://releases.hashicorp.com/terraform/] to get the latest release of terraform

- Download the latest version (`linux-amd-64`) into the `~/User/bin` using `wget` and unzip the file 

- Setup the service account keys using SFTP

- - Find the location of the saved keys from the service account created. Navigate to that folder -
- - Since we have access to the `de-zoomcamp` host using SSH, we can run in the keys folder

```bash
sftp de-zoomcamp
```

- - Navigate to home directory using the remote host and create a new hidden folder `.gc` that contains the service account keys. Run `put service-key-name.json`

- - Set GOOGLE_APPLICATION_CREDENTIALS to point to the file 

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/service-key-name.json

gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```




## Running our week 1 postgres, pgadmin on this instance

- Navigate to `~/data_engineering_zoomcamp_2025/01_docker_terraform/2_docker_sql` and run the docker compose command in detached mode `docker-compose up -d`

You will notice that pgadmin and postgress images will be pulled and starting to run

- Installing the pgcli (same instructions as week1)

```bash
pip install pgcli
```

If you have problems installing `pgcli` with the command above, try this:

```bash
conda install -c conda-forge pgcli
pip install -U mycli
```
Using `pgcli` to connect to Postgres

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Connecting the postgres instance to our local machine

1) Run the `docker ps` command to ensure all the contianers running in the instance 
2) Now open the terminal in vscode in the remote window > ports > forward the `5432` port and `8080`

We can now essentially run the above `pgcli` command from anywhere outside the remote window in our local terminal! Secondly, we can now access the `localhost:8080` to login into pgadmin. 

3) Navigate to the jupyter notebook in remote window and start jupyter notebook `jupyter notebook`. Once it starts forward yet another port `8888` and open in the local machine. 