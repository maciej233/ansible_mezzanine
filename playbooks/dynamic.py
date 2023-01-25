"""The program generate dynamic inventory from vagrant machines"""
import argparse
import textwrap
import paramiko
import subprocess
import json
import sys

"""Create user interface"""
def parse_args():
    parser = argparse.ArgumentParser(prog="dynamic",
                                    description="Vagrant inventory script",
                                    epilog=textwrap.wrap("""
                                    host - list of running 
                                    list - list of running hosts
                                    """))
    group = parser.add_mutually_exclusive_group(required=True)  # only one argument can be parsed at once
    group.add_argument("--list", action="store_true")
    group.add_argument("--host")
    return parser.parse_args()

"""Get running hosts"""
def running_hosts_list():
    cmd = "vagrant status --machine-readable"
    process = subprocess.check_output(cmd.split(), encoding="UTF-8").rstrip()
    hosts = []
    for line in process.split("\n"):
        (_, host, state, running, *_) = line.split(",")
        if state == "state" and running == "running":
            hosts.append(host)
    return hosts

"""Return host's details"""
def hosts_detail(host):
    cmd = "vagrant ssh-config {}".format(host)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, encoding="UTF-8")
    config = paramiko.SSHConfig()
    config.parse(process.stdout)
    result = config.lookup(host)
    return {
        'ansible_ssh_host': result["hostname"],
        'ansible_ssh_port': result["port"],
        'ansible_ssh_user': result["user"],
        'ansible_ssh_private_key_file': result["identityfile"][0]
    }

if __name__== "__main__":
    args = parse_args()
    if args.list:
        hosts = running_hosts_list()
        json.dump({'vagrant': hosts}, sys.stdout)
    else:
        detailed_host = hosts_detail(args.host)
        json.dump(detailed_host, sys.stdout)    