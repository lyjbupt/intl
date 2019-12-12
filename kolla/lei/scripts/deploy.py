import argparse
import configparser
import os
import shutil
import subprocess

from git import Repo
import yaml

WORK_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_INVENTORY = 'kolla-ansible/ansible/inventory/'
DEFAULT_GLOBALS = 'kolla-ansible/etc/kolla/globals.yml'
KOLLA_ANSIBLE_REPO = 'https://github.com/openstack/kolla-ansible.git'
KOLLA_ANSIBLE_CMD = 'kolla-ansible/tools/kolla-ansible'


def provision_deploy_node(conf):
    os.chdir(WORK_DIR)
    if not conf.deploy_only:
        install_kolla_ansible(conf)
        generate_inventory(conf)
        generate_ansible_conf(conf)
        generate_conf(conf)
        bootstrap_server(conf)
        prechecks(conf)
    deploy(conf)

def install_kolla_ansible(conf):
    repo_path = os.path.join(WORK_DIR, 'kolla-ansible')
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    repo = Repo.clone_from(
        KOLLA_ANSIBLE_REPO,
        repo_path)
    release = conf.kolla_ansible_conf.get('openstack_release') or 'master'

    # If user requests OpenStack release other than master
    # checkout corresponding branch
    if release != 'master':
        repo.git.checkout('--track', 'origin/stable/{}'.format(release))
    subprocess.run(
        'pip3 install -r kolla-ansible/requirements.txt',
        shell=True,
        check=True
    )
    subprocess.run('sudo mkdir -p /etc/kolla', shell=True, check=True)
    subprocess.run('sudo chown $USER:$USER /etc/kolla', shell=True, check=True)
    subprocess.run(
        'cp -r kolla-ansible/etc/kolla/* /etc/kolla',
        shell=True,
        check=True
    )


def generate_inventory(conf):
    if len(conf.compute_nodes) == 1 \
            and conf.controller_nodes[0] == conf.compute_nodes[0]:
        inventory_file = 'all-in-one'
    else:
        inventory_file = 'multinode'

    inventory_parser = configparser.ConfigParser(allow_no_value=True)
    inventory_parser.read(os.path.join(
        DEFAULT_INVENTORY, inventory_file))

    if inventory_file == 'multinode':
        # For stable/queens and stable/rocky, use external-compute
        for section in (
                'control', 'network', 'monitoring', 'compute', 'storage'):
            for name in inventory_parser[section]:
                inventory_parser.remove_option(section, name)

        for control_section in ('control', 'network', 'monitoring'):
            inventory_parser.set(control_section, conf.controller_nodes[0])

        for compute_node in conf.compute_nodes:
            # For stable/queens and stable/rocky, use external-compute
            inventory_parser.set('compute', compute_node)

    with open(os.path.join(WORK_DIR, inventory_file), 'w') as config_file:
        inventory_parser.write(config_file, space_around_delimiters=False)


def generate_ansible_conf(conf):
    ansible_parser = configparser.ConfigParser(allow_no_value=True)
    ansible_parser.add_section("defaults")

    for ansible_settings in conf.ansible_conf:
        ansible_parser.set("defaults", ansible_settings, conf.ansible_conf[ansible_settings])

    with open(os.path.join(WORK_DIR, "./ansible.cfg"), 'w') as f:
        ansible_parser.write(f, space_around_delimiters=False)

def generate_conf(conf):
    with open('/etc/kolla/globals.yml', 'w') as global_file:
        yaml.dump(dict(conf.kolla_ansible_conf), global_file)

    subprocess.run(
        './kolla-ansible/tools/generate_passwords.py',
        shell=True,
        check=True
    )


def bootstrap_server(conf):
    subprocess.run(
        './{} -i {} bootstrap-servers'.format(
            KOLLA_ANSIBLE_CMD, conf.inventory_file),
        shell=True,
        check=True
    )


def prechecks(conf):
    subprocess.run(
        './{} -i {} prechecks'.format(KOLLA_ANSIBLE_CMD, conf.inventory_file),
        shell=True,
        check=True
    )


def deploy(conf):
    subprocess.run(
        './{} -i {} deploy'.format(KOLLA_ANSIBLE_CMD, conf.inventory_file),
        shell=True,
        check=True
    )
    subprocess.run(
        './{} -i {} post-deploy'.format(
            KOLLA_ANSIBLE_CMD, conf.inventory_file),
        shell=True,
        check=True
    )


class Config(object):

    def __init__(self, config_file='', deploy_only=False):
        self.config_file = config_file
        self.parser = configparser.ConfigParser(allow_no_value=True)
        self.compute_nodes, self.controller_nodes = [], []
        self.ansible_conf = None
        self.kolla_ansible_conf = None
        self.inventory_file = 'all-in-one'
        self.deploy_only = deploy_only
        self.parse_config()

    def parse_config(self):
        self.parser.read(self.config_file)
        self.compute_nodes.extend(list(self.parser['compute'].keys()))
        self.controller_nodes.extend(list(self.parser['controller'].keys()))
        self.ansible_conf = self.parser['ansible']
        self.kolla_ansible_conf = self.parser['kolla-ansible']
        if len(self.compute_nodes) == 1 \
                and self.controller_nodes[0] == self.compute_nodes[0]:
            self.inventory_file = 'all-in-one'
        else:
            self.inventory_file = 'multinode'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='quickly setup kolla deployment')

    parser.add_argument('--config-file', dest='config_file', required=True,
                        help='path of config file with info of the deployment')
    parser.add_argument('--deploy-only', dest='deploy_only', required=False, default=False,
                        action='store_true',
                        help='if specified, skip bootstrap and check phase, deploy directly')
    args = parser.parse_args()
    provision_deploy_node(Config(**vars(args)))

