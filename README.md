# Ansible dynamic inventory demo

At the time of writing this, the Ansible documentation is fairly sparse and doesn't provide a lot of details about how dynamic script inventories relate to and differ from flat file inventory host format extensions such as `.ini` or `.yaml`. The JSON object (and deserialised python dict) a dynamic inventory script needs to produce looks somewhat different in schema and structure compared to the static flat file formats.

Clone this gist and run `./demo.sh` as an example. It demonstrates a few things:

- `eg_hosts.json` is a contrived example to tease out the combinations between hosts, groups, and children groupings.
  - `demo_dynamic_inventory.py` simply reads this into an inventory dict, as if it was something an API or script would product.
- `./demo.sh` provides ansible related commands to help debug and inspect how the inventory is being interpreted.
- Demonstrates how inventory directories such as `group_vars` and `host_vars` can overload/add to vars from dynamic inventories.

## Lessons

### Nested group hierarchy is not supported in dynamic scripts

Ansible YAML inventory files permit nested grouping with sub-groups as children of parent groups, but dynamic inventory JSON input does not permit nesting. Dynamic inventory has to flatten out group definitions. E.g. this is a valid nested static inventory:

```yaml
multi_region_bc:
  children:
    region_b:
      hosts:
        h1.region_b.test:
        h2.region_b.test:
    region_c:
      children:
        subdomain_c1:
          hosts:
            h1.subdomain_c1.region_c.test:
        subdomain_c2:
          hosts:
            h1.subdomain_c2.region_c.test:
```

Running `ansible-inventory -i eg_nested_hosts.yml --list`, shows the nesting gets flattended down. The above needs to converted into this:

```json
{
  "multi_region_bc":
  {
    "children": [
      "region_b",
      "region_c"
    ]
  },
  "region_b": {
    "hosts": [
      "h1.region_b.test",
      "h2.region_b.test"
    ]
  },
  "region_c": {
    "children": [
      "subdomain_c1",
      "subdomain_c2"
    ]
  },
  "subdomain_c1": {
    "hosts": [
      "h1.subdomain_c1.region_c.test"
    ]
  },
  "subdomain_c2": {
    "hosts": [
      "h1.subdomain_c2.region_c.test"
    ]
  }
}
```

## Related

- [Developing dynamic inventory: Inventory scripts](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-inventory-scripts)
- [ansible-inventory](https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html#ansible-inventory)
  - Useful to see how your inventroy is interpreted by ansible.
  - Expands and permutates group variables into the host variables - see the need for a `_meta` node.
- [Creating custom dynamic inventories for Ansible](https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible)
- [geerlingguy / ansible-for-devops / inventory.py](https://github.com/geerlingguy/ansible-for-devops/blob/master/dynamic-inventory/custom/inventory.py)
