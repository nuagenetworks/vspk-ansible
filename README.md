# VSPK-Ansible

## Overview
The nuage_vspk module for Ansible allows you to manage or find Nuage VSP entities, including:

* Create
* Update
* Delete
* Assign
* Unassign
* Search for an entity
* Wait for a job to finish
* Change passwords on users (can not be done through regular update)
* Wait for a job

More details on the [Wiki](https://github.com/nuagenetworks/vspk-ansible/wiki)

## Trying the module
1. Clone this repository onto a machine with Ansible and VSPK-Python installed, which has access to your VSD.
2. Adapt the `nuage-vspk-tests.yml` file to reflect your environment and the roles you want to execute
3. From within the repository folder, execute `ansible-playbook nuage-vspk-tests.yml`

## Special considerations
* `type` and `parent_type` are the CamelCase values of the classes in the Python VSPK (without the `NU` part). Example, a domain template should be mentioned as `DomainTemplate`, as can seen in the [Domain Template VSPK doc](https://nuagenetworks.github.io/vspkdoc/html/v4_0/nudomaintemplate.html): `nudomaintemplate.NU`**`DomainTemplate`**`(bambou.nurest_object.NUMetaRESTObject,)`.
* `properties` should be represented by there lowercase-underscore names, as documented in the [Nuage Python VSPK docs](https://nuagenetworks.github.io/vspkdoc/html/index.html).
* `match_filter` is used as a way of finding a specific entiy (if no `id` is specified), if this is omitted, a filter is build based on all `properties`, which in most cases will fail. 
* For the `match_filter`, the filter should use the camelCase names of the properties as in the [Nuage API docs](https://nuagenetworks.github.io/vsd-api-documentation/v4_0/), for instance: `name == 'Allow all policy' and policyState == 'DRAFT'`.

### Useful links
* [Nuage Python VSPK docs](https://nuagenetworks.github.io/vspkdoc/html/index.html)
* [Nuage API docs](https://nuagenetworks.github.io/vsd-api-documentation/v4_0/)

## Examples
The roles folder holds two roles that serve as examples. The basic role will show each functionality available for the module, creating, updating, assigning, unassigning and deleting entities.

The advanced role will create a Enterprise with an admin user,  a domain template which holds 3 zones, 3 subnets, an ingress, egress and forward policy setup and 2 domains instantiated from the domain template. After this, it will pause so you can verify ths in your Nuage VSD Architect. When pressing enter, the role will clean up after itself. Aborting instead and running again will demonstrate idempotency.

## State
This module is in active development and in **beta** stage. As such, this module is not officially supported from a Nuage Networks product perspective.

## Tested with
* Nuage 4.0R5 and VSPK-Python 4.0.5
* Nuage 4.0R7 and VSPK-Python 4.0.7
* Nuage 4.0R8 and VSPK-Python 4.0.8
* Nuage 5.0.1 and VSPK-Python 5.0.1
* [NuageX](https://nuagex.io) (Nuage 4.0R5 and VSPK-Python 4.0.5)
* Ansible 2.3

## Requirements
* Ansible 2.3
* VSPK-Python matching your Nuage VSP environment
* Nuage VSP 4.0Rx, 5.x.x

