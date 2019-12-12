#!/usr/bin/env python

import os
import ConfigParser
import sys
import click
import re
import json
from subprocess import call

def read_config_file(filename):  
    '''Read_config_file(filename) 
        this function is used for parse the config file'''      
    data = {}  
    config = ConfigParser.ConfigParser()  
    try:  
        with open(filename,'r') as confile:  
            config.readfp(confile)  
            for i in config.sections():  
                for (key, value) in config.items(i):  
                    data[key] = value  
            return data      
    except Exception:  
        print "Open config file %s error."%filename

def run_and_check(cmd):
    print "Running %s now..." %(cmd)
    try:
    	retcode = call(cmd, shell=True)
    	if retcode < 0:
	    print "Command was terminated by signal", -retcode
        elif retcode > 0:
	    print "Command returned", retcode
	    sys.exit("Command execution failed!")
    	else:
	    print "Command returned", retcode
    
    except OSError, e:
	print "Execution failed:", e

def update_ka_invertory(ka_config, config):
    compute_list = config['compute_nodes'].strip().split('|')
    compute_user = config['compute_user'].strip().split('|')
    control_list = config['control_nodes'].strip()
    control_user = config['control_user'].strip()
    ctrl_subst = control_list + ' ansible_user=' + control_user + ' ansible_become=true' 
    compute_pair = map(lambda x,y:[x,y], compute_list ,compute_user)
    cmpu_subst = '' 
    for i in compute_pair:
	cmpu_subst += ' ansible_user='.join(i)
	cmpu_subst += ' ansible_become=true\n'
    
    with open(ka_config, 'r+') as f:
	src = f.read()
	dest_s1 = re.sub(r'^\[control\].*?^\[', r'[control]\n'+ctrl_subst+'\n[', src, 0, re.S | re.M)
	dest_s2 = re.sub(r'^\[network\].*?^\[', r'[network]\n[', dest_s1, 0, re.S | re.M)
	dest_s3 = re.sub(r'^\[compute\].*?^\[', r'[compute]\n'+cmpu_subst+'\n[', dest_s2, 0, re.S | re.M)
	dest_s4 = re.sub(r'^\[monitoring\].*?^\[', r'[monitoring]\n'+control_list+'\n[', dest_s3, 0, re.S | re.M)
	final_str = re.sub(r'^\[storage\].*?^\[', r'[storage]\n[', dest_s4, 0, re.S | re.M)
	f.seek(0, 0)
	f.truncate()
	f.write(final_str)
	f.close()


def deploy_stack(phase, config): 
    if phase == 'openstack':
        click.echo('Performing DEPLOY of %s using config %s!' %(phase,config))
	p = read_config_file(config)
	for cmd in rh_yum_prep:
	    run_and_check(cmd)
	print "Switching to kolla_ansible working directoy %s..." %ka_root
	os.chdir(ka_root)
	for cmd in rh_kolla_dev:
	    run_and_check(cmd)
	print "Configing Ansible..."
	for cmd in rh_ansible_config:
	    run_and_check(cmd)
	print "Configing Kolla Ansible inventory at %s..." %ka_root
	update_ka_invertory(ka_config, p)
	print "Verfiying ansible connection at %s..." %ka_root
	cmd = "ansible -i " + ka_config + " all -m ping"
	run_and_check(cmd)
	os.chdir(ka_tools)
	print "Generating Kolla passwords..."
	for cmd in rh_kolla_passwd_gen_dev:
	    run_and_check(cmd)
	os.chdir(ka_root)
	print "Config Kolla global settings at %s..." %ka_root
	for cmd in rh_kolla_global_dev:
	    run_and_check(cmd)
	cmd = "sudo sed -i 's/^kolla_internal_vip_address.*$/kolla_internal_vip_address\: \""+p['control_nodes'].strip()+"\"/' /etc/kolla/globals.yml"
	run_and_check(cmd)
	os.chdir(ka_tools)
	print "Start Kolla-Ansible deploy..."
	for cmd in rh_ka_deploy_dev:
	    run_and_check(cmd)
	os.chdir(ka_tools)
	print "Initialising Openstack at %s..." %ka_root
	for cmd in rh_pip_post:
	    run_and_check(cmd)
	
    else:
	print "Phase %s to be defined." %phase

ka_root = os.getenv("HOME")
ka_tools = ka_root+'/kolla-ansible/tools'
ka_config = "multinode"
ansible_cfg = "/etc/ansible/ansible.cfg"
kolla_glb_cfg = "/etc/kolla/globals.yml"
intel_env = True
rh_yum_prep = [
    "sudo yum -y install epel-release",
    "sudo yum -y install python-devel libffi-devel gcc openssl-devel libselinux-python",
    "sudo yum -y install python-pip",
    "sudo pip install -U pip",
    "sudo yum -y install ansible",
]

rh_kolla_dev = [
    "git clone https://github.com/openstack/kolla",
    "git clone https://github.com/openstack/kolla-ansible",
    "sudo pip install -r kolla/requirements.txt",
    "sudo pip install -r kolla-ansible/requirements.txt",
    "sudo mkdir -p /etc/kolla",
    "sudo chown $USER:$USER /etc/kolla",
    "cp -r kolla-ansible/etc/kolla/* /etc/kolla",
    "cp kolla-ansible/ansible/inventory/* .",
]

rh_ansible_config = [
    "sudo cp " + ansible_cfg + " " + ansible_cfg +".orig",
    "sudo sed -i '/^#host_key_checking/s/^#//' " + ansible_cfg,
    "sudo sed -i '/^#pipelining/s/^#//' " + ansible_cfg,
    "sudo sed -i '/^#forks/s/^#//;s/forks.*$/forks = 100/' " + ansible_cfg,
]
if intel_env:
    rh_ansible_config.append("sudo sed -i '/^#remote_user/s/^#//;s/remote_user.*$/remote_user = centos/' " + ansible_cfg)
else:
    print "Please set ssh information for kolla-ansible in ansible.cfg accordingly..."

rh_kolla_passwd_gen_dev = [
    "sudo ./generate_passwords.py",
]

rh_kolla_global_dev = [
    "sudo cp " + kolla_glb_cfg + " " + kolla_glb_cfg + ".orig",
    "sudo sed -i '/^#kolla_base_distro/s/^#//' " + kolla_glb_cfg,
    "sudo sed -i '/^#kolla_install_type/s/^#//;s/kolla_install_type.*$/kolla_install_type\: \"source\"/' " + kolla_glb_cfg,
    "sudo sed -i '/^#openstack_release/s/^#//;s/openstack_release.*$/openstack_release\: \"master\"/' " + kolla_glb_cfg,
    "sudo sed -i '/^#enable_haproxy/s/^#//;s/^enable_haproxy.*$/enable_haproxy\: \"no\"/' " + kolla_glb_cfg,
    "sudo sed -i '/^#network_interface/s/^#//;s/^network_interface.*$/network_interface\: \"eth0\"/' " + kolla_glb_cfg,
]
if intel_env:
	rh_kolla_global_dev.append("sudo sed -i '/^#neutron_external_interface/s/^#//;s/^neutron_external_interface.*$/neutron_external_interface\: \"tap0\"/' " + kolla_glb_cfg)
else:
    print "Please set external interface information for kolla-ansible in globals.yml accordingly..."

rh_ka_deploy_dev = [
    "./kolla-ansible -i ../../"+ka_config+" bootstrap-servers",
    "./kolla-ansible -i ../../"+ka_config+" prechecks",
    "./kolla-ansible -i ../../"+ka_config+" deploy",
]

rh_pip_post = [
    "sudo pip install python-openstackclient",
    "./kolla-ansible post-deploy",
    ". /etc/kolla/admin-openrc.sh && ./init-runonce",
]

@click.command()
@click.argument('action')
@click.argument('phase')
@click.option('--config', '-c', help='location of input config file')
def main(action, phase, config):
    if action == 'deploy':
        deploy_stack(phase, config)
    else:
	print "Action %s to be defined." %action

if __name__ == "__main__":
    main()
