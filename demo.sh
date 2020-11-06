#!/usr/bin/env bash
set -e

echo -e '\n# Input JSON demo inventory example'
cat eg_dynamic_hosts.json

echo -e '\n# How ansible interprets and expands the inventory showing which vars apply where'
ansible-inventory -i demo_dynamic_inventory.py --list

echo -e '\n# Debug and show ansible group var'
ansible localhost -i demo_dynamic_inventory.py -m debug -a 'var=groups'

echo -e '\n# Using demo dynamic inventory script to list all hosts'
ansible -i demo_dynamic_inventory.py --list all

echo -e '\n# Using demo dynamic inventory script to list hosts that need a jump box'
ansible -i demo_dynamic_inventory.py --list jump

echo -e '\n# Using demo dynamic inventory script to list hosts for a specific region region_a'
ansible -i demo_dynamic_inventory.py --list region_a

echo -e '\n# Using demo dynamic inventory script to list hosts for a multi-regional grouping'
ansible -i demo_dynamic_inventory.py --list multi_region_bc

echo -e '\n# Using demo dynamic inventory script to list hosts that need a special SSH proxy command to use a jump/bastion host'
ansible -i demo_dynamic_inventory.py --list jump