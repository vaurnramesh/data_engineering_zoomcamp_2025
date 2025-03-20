## Create SSH Directory

- Create an `.ssh` directory on your local machine.  
- Follow this [guide](https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos) to generate an SSH key in your `.ssh` directory.  
- Use the public key to upload it to your Google account.  


## Create a VM instance

- Create an instance in the region you are located in 
- Changed the OS to Ubuntu and allocated 20GB
- Change the external IP from `ephemeral` to a `static` external IP to prevent editing the config in the `.ssh` everytime
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

To install docker in the instance - 
- `sudo apt-get update`
- `sudo apt-get install docker.io`

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

### Cloning this repo in our instance

`git clone https://github.com/vaurnramesh/data_engineering_zoomcamp_2025.git`

