# kolla-quick-setup

Script for quickly setting up a kolla deployment.

Only Python3 is supported.

## Usage:

It is highly recommended to use a virtual environment to run the script:
```
python3 -m venv {{env_path}}
source {{env_path}}/bin/activate
```

Install python dependencies:
```
pip3 install -r requirements.txt
```

Execute the script with your config file, the repo ships with an example conf you could consult:
```
python3 scripts/deploy.py --config-file example.ini
```
A typical config's structure is similar to a INI file, which consists of three sections: compute, controller and kolla-ansible.
You should specify compute and controller hosts in compute and controller sections. Options in kolla-ansible section will be used
to produce globals.yml file for kolla ansible deploy. So the option name and value are exactly identical to globals.yml.

The script will install kolla-ansible, generate related configs, bootstrap servers and deploy automatically. You have to make
sure the deploy host can ssh to all the OpenStack nodes and the account are in the sudoer list.

If everything goes well you'll get a newly deployed OpenStack environment,
then you can execute kolla ansible script to initialize network and flavor:
```
./kolla-quick-setup/scripts/kolla-ansible/tools/init-runonce
