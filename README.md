# VSPK-Ansible

## Overview
The nuage_vspk module for Ansible allows you to manage or find Nuage VSP entities, including:

* Create
* Update
* Delete
* Assign
* Unassign
* Search for an entity
* Change passwords on users (can not be done through regular update)

More details on the [Wiki](https://github.com/nuagenetworks/vspk-ansible/wiki)

## Trying the module
1. Clone this repository onto a machine with Ansible and VSPK-Python installed, which has access to your VSD.
2. Adapt the ``nuage-vspk-tests.yml`` file to reflect your environment and the roles you want to execute
3. From within the repository folder, execute ``ansible-playbook nuage-vspk-tests.yml``

## Examples
The roles folder holds two roles that serve as examples. The basic role will show each functionality available for the module, creating, updating, assigning, unassigning and deleting entities.

The advanced role will create a Enterprise with an admin user,  a domain template which holds 3 zones, 3 subnets, an ingress, egress and forward policy setup and 2 domains instantiated from the domain template. After this, it will pause so you can verify ths in your Nuage VSD Architect. When pressing enter, the role will clean up after itself. Aborting instead and running again will demonstrate idempotency.

## Tested with
* Nuage 4.0R7 and VSPK-Python 4.0.7
* [NuageX](https://nuagex.io) (Nuage 4.0R5 and VSPK-Python 4.0.5)
* Ansible 2.2

## Requirements
* Ansible 2
* VSPK-Python matching your Nuage VSP environment
* Nuage VSP 4.0Rx

