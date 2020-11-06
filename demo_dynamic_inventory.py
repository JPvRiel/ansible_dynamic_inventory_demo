#!/usr/bin/env python

## See https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#inventory-script-conventions

import os
import sys
import argparse
import json

class DemoInventory(object):


  def __init__(self):
    self.inventory = {}
    self.read_cli_args()

    # Called with `--list`.
    if self.args.list:
        self.inventory = self.example_as_json()
    # Called with `--host [hostname]`.
    elif self.args.host:
        # Not implemented, since we return _meta info `--list`.
        self.inventory = self.empty_inventory()
    # If no groups or vars are present, return an empty inventory.
    else:
        self.inventory = self.empty_inventory()

    print json.dumps(self.inventory)


  # Empty inventory for testing.
  def empty_inventory(self):
    return {'_meta': {'hostvars': {}}}


  # Demo from JSON file
  def example_as_json(self):
    with open('eg_dynamic_hosts.json', 'r') as json_file:
      return json.load(json_file)


  # Read the command line args passed to the script.
  def read_cli_args(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store')
    self.args = parser.parse_args()


# Get the inventory.
DemoInventory()