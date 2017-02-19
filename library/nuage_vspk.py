#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: nuage_vspk
short_description: Manage Nuage VSP environments
description:
    - Manage or find Nuage VSP entities, this includes create, update, delete, assign, unassign, find one and find all, with all supported properties.
version_added: "2.2"
author: Philippe Dellaert (@pdellaert)
options:
    api_username:
        description:
            - The username to connect to the Nuage VSP environment (example csproot).
        required: true
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    api_password:
        description:
            - The password to connect to the Nuage VSP environment (example csproot).
        required: true
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    api_enterprise:
        description:
            - The enterprise to connect to the Nuage VSP environment (example csp).
        required: true
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    api_url:
        description:
            - The URL to connect to the Nuage VSP environment (example https://10.0.0.1:8443).
        required: true
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    type:
        description:
            - The type of entity you want to work on (example Enterprise).
            - This should match the objects CamelCase class name in VSPK-Python.
            - This Class name can be found on U(https://nuagenetworks.github.io/vspkdoc/html/index.html).
        required: true
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    id:
        description:
            - The ID of the entity you want to work on.
            - In combination with I(find), it will only return the single entity.
            - In combination with I(state), it will either update or delete this entity.
            - Will take precedence over properties whenever an entity needs to be found.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    parent_id:
        description:
            - The ID of the parent of the entity you want to work on.
            - When I(state) is specified, the entity will be gathered from this parent, if it exists, unless an I(id) is specified.
            - When I(find) is specified, the entity will be searched for in this parent, unless an I(id) is specified.
            - If specified, I(parent_type) also needs to be specified.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    parent_type:
        description:
            - The type of parent the ID is specified for (example Enterprise).
            - This should match the objects CamelCase class name in VSPK-Python.
            - This Class name can be found on U(https://nuagenetworks.github.io/vspkdoc/html/index.html).
            - If specified, I(parent_id) also needs to be specified.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
    state:
        description:
            - Specifies the desired state of the entity.
            - If I(state=present), in case the entity already exists, will update the entity if it needed.
            - If I(state=present), in case the relationship with the parent is a member relationship, will assign the entity as a member of the parent, if needed.
            - If I(state=absent), in case the relationship with the parent is a member relationship, will unassign the entity as a member of the parent, if needed.
            - Either I(state) or I(find) needs to be defined, both can not be defined at the same time.
        required: false
        default: null
        choices:
            - present
            - absent
        aliases: []
        version_added: "1.0"
    find:
        description:
            - Specifies whether to return the first matching entity or all.
            - If I(parent_id) and I(parent_type) are defined, will only search within the parent. Otherwise, if allowed, will search in the root object.
            - If I(id) is specified, will only return the single entity matching the id.
            - Otherwise, if I(properties) are defined, it will do an AND search using all properties.
            - When searching for an entity, it is advised to provide the minimal required I(properties) to identify it.
            - Either I(state) or I(find) needs to be defined, both can not be defined at the same time.
        required: false
        default: null
        choices:
            - one
            - all
        aliases: []
        version_added: "1.0"
    properties:
        description:
            - Properties are the key, value pairs of the different properties an entity has.
            - If no I(id) is specified, these are used to find or determine if the entity exists.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: "1.0"
notes:
    - Check mode is supported, but with some caveats.
    - It will not do any changes, and if possible try to determine if it is able do what is requested.
    - In case a parent id is provided from a previous task, it might be empty and if a search is possible on root, it will do so, which can impact performance.
requirements:
    - Supports Nuage VSP 4.0Rx
    - Proper VSPK-Python installed for your Nuage version
'''

EXAMPLES = '''
# This can be executed as a single role, with the following vars
# vars:
#   nuage_api_username: csproot
#   nuage_api_password: csproot
#   nuage_api_enterprise: csp
#   nuage_api_url: https://10.0.0.254:8443
#   enterprise_name: Ansible-Enterprise
#   enterprise_new_name: Ansible-Updated-Enterprise

# Creating a new enterprise
- name: Create Enterprise
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: Enterprise
    state: present
    properties:
      name: "{{ enterprise_name }}"
  register: nuage_enterprise

# Updating an enterprise's name
- name: Update Enterprise name
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: Enterprise
    id: "{{ nuage_enterprise.id }}"
    state: present
    properties:
      name: "{{ enterprise_new_name }}"

# Creating a User in an Enterprise
- name: Create admin user
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: User
    parent_id: "{{ nuage_enterprise.id }}"
    parent_type: Enterprise
    state: present
    properties:
      email: "ansible@localhost"
      first_name: "Ansible"
      last_name: "Admin"
      password: "ansible"
      user_name: "ansible-admin"
  register: nuage_user

# Finding a group in an enterprise
- name: Find Administrators group in Enterprise
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: Group
    parent_id: "{{ nuage_enterprise.id }}"
    parent_type: Enterprise
    find: one
    properties:
      name: "Administrators"
  register: nuage_group

# Assign the user to the group
- name: Assign admin user to administrators
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: User
    id: "{{ nuage_user.id }}"
    parent_id: "{{ nuage_group.id }}"
    parent_type: Group
    state: present

# Creating multiple DomainTemplates
- name: Create DomainTemplate
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: DomainTemplate
    parent_id: "{{ nuage_enterprise.id }}"
    parent_type: Enterprise
    state: present
    properties:
      name: "{{ item }}"
      description: "Created by Ansible"
  with_items:
    - "Template-1"
    - "Template-2"

# Finding all DomainTemplates
- name: Fetching all DomainTemplates
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: DomainTemplate
    parent_id: "{{ nuage_enterprise.id }}"
    parent_type: Enterprise
    find: all
  register: nuage_domain_templates

# Deleting all DomainTemplates
- name: Deleting all found DomainTemplates
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: DomainTemplate
    state: absent
    id: "{{ item.ID }}"
  with_items: "{{ nuage_domain_templates.entities }}"
  when: nuage_domain_templates.entities is defined

# Unassign user from group
- name: Unassign admin user to administrators
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: User
    id: "{{ nuage_user.id }}"
    parent_id: "{{ nuage_group.id }}"
    parent_type: Group
    state: absent

# Deleting an enterprise
- name: Delete Enterprise
  connection: local
  nuage_vspk:
    api_username: "{{ nuage_api_username }}"
    api_password: "{{ nuage_api_password }}"
    api_enterprise: "{{ nuage_api_enterprise }}"
    api_url: "{{ nuage_api_url }}"
    type: Enterprise
    id: "{{ nuage_enterprise.id }}"
    state: absent
'''

RETURN = '''
id:
    description: The id of the entity that was found, created, updated or assigned
    returned: I(state=present) and I(find=one) in case an entity was found
    type: string
    sample: bae07d8d-d29c-4e2b-b6ba-621b4807a333
entities:
    description: A list of entities handled. Each element is the to_dict() of the entity.
    returned: I(state=present) and I(find), with only one element in case of I(state=present) or I(find=one)
    type: list
    sample: [{
        "ID": acabc435-3946-4117-a719-b8895a335830",
        "assocEntityType": "DOMAIN",
        "command": "BEGIN_POLICY_CHANGES",
        "creationDate": 1487515656000,
        "entityScope": "ENTERPRISE",
        "externalID": null,
        "lastUpdatedBy": "8a6f0e20-a4db-4878-ad84-9cc61756cd5e",
        "lastUpdatedDate": 1487515656000,
        "owner": "8a6f0e20-a4db-4878-ad84-9cc61756cd5e",
        "parameters": null,
        "parentID": "a22fddb9-3da4-4945-bd2e-9d27fe3d62e0",
        "parentType": "domain",
        "progress": 0.0,
        "result": null,
        "status": "RUNNING"
        }]
'''

try:
    from vspk import v4_0 as vsdk
    from vspk.v4_0 import fetchers
    from bambou.exceptions import BambouHTTPError

    HASVSPK = True
except ImportError:
    HASVSPK = False


class NuageEntityManager(object):
    """
    This module is meant to manage an entity in a Nuage VSP Platform
    """

    def __init__(self, module):
        self.module = module
        self.api_username = module.params['api_username']
        self.api_password = module.params['api_password']
        self.api_enterprise = module.params['api_enterprise']
        self.api_url = module.params['api_url']
        self.type = module.params['type']

        self.state = None
        if 'state' in module.params.keys():
            self.state = module.params['state']

        self.find = None
        if 'find' in module.params.keys():
            self.find = module.params['find']

        self.id = None
        if 'id' in module.params.keys():
            self.id = module.params['id']

        self.parent_id = None
        if 'parent_id' in module.params.keys():
            self.parent_id = module.params['parent_id']

        self.parent_type = None
        if 'parent_type' in module.params.keys():
            self.parent_type = module.params['parent_type']

        self.properties = None
        if 'properties' in module.params.keys():
            self.properties = module.params['properties']

        self.entity = None
        self.entity_class = None
        self.parent = None
        self.parent_class = None
        self.entity_fetcher = None

        self.result = {
            'state': self.state,
            'id': self.id,
            'entities': []
        }
        self.nuage_connection = None

        self.verify_input()
        self.connect_vspk()
        self.handle_parent()

    def connect_vspk(self):
        """
        Connects to a Nuage API endpoint
        """
        try:
            # Connecting to Nuage
            self.nuage_connection = vsdk.NUVSDSession(username=self.api_username, password=self.api_password,
                                                      enterprise=self.api_enterprise, api_url=self.api_url)
            self.nuage_connection.start()
        except BambouHTTPError, e:
            self.module.fail_json(
                msg='Unable to connect to the API URL with given username, password and enterprise: {0}'.format(e))

    def verify_input(self):
        """
        Verifies the parameter input for types and parent correctness and necessary parameters
        """
        # Checking if type exists
        try:
            self.entity_class = getattr(vsdk, 'NU{0:s}'.format(self.type))
        except AttributeError:
            self.module.fail_json(msg='Unrecognised type specified')

        if self.module.check_mode:
            return

        if self.parent_id and not self.parent_type:
            # Checking if parent info is ok
            self.module.fail_json(msg='Parent ID specified, but no parent type specified')
        elif self.parent_type and not self.parent_id:
            # Checking if parent info is ok
            self.module.fail_json(msg='Parent type specified, but no parent id specified')
        elif self.parent_type:
            # Checking if parent type exists
            try:
                self.parent_class = getattr(vsdk, 'NU{0:s}'.format(self.parent_type))
            except AttributeError:
                # The parent type does not exist, fail
                self.module.fail_json(msg='Unrecognised parent type specified')

            fetcher = self.parent_class().fetcher_for_rest_name(self.entity_class.rest_name)
            if fetcher is None:
                # The parent has no fetcher, fail
                self.module.fail_json(msg='Specified parent is not a valid parent for the specified type')
        elif not self.id:
            # If there is an id, we do not need a parent because we'll interact directly with the entity
            # If an assign needs to happen, a parent will have to be provided
            # Root object is the parent
            self.parent_class = vsdk.NUMe
            fetcher = self.parent_class().fetcher_for_rest_name(self.entity_class.rest_name)
            if fetcher is None:
                self.module.fail_json(msg='No parent specified and root object is not a parent for the type')

        # Verifying state or find is set:
        if not self.find and not self.state:
            self.module.fail_json(msg='You have to define either a state or a find statement')

        # Verifying state and properties if required
        if not self.id and not self.properties and self.find not in ['one', 'all']:
            self.module.fail_json(msg='Unable to execute without an id or some properties')

    def handle_parent(self):
        """
        Fetches the parent if needed, otherwise configures the root object as parent. Also configures the entity fetcher
        Important notes:
        - If the parent is not set, the parent is automatically set to the root object
        - It the root object does not hold a fetcher for the entity, you have to provide an ID
        - If you want to assign/unassign, you have to provide a valid parent
        """
        self.parent = self.nuage_connection.user

        if self.parent_id:
            self.parent = self.parent_class(id=self.parent_id)
            try:
                self.parent.fetch()
            except BambouHTTPError, e:
                self.module.fail_json(msg='Failed to fetch the specified parent: {0}'.format(e))

        self.entity_fetcher = self.parent.fetcher_for_rest_name(self.entity_class.rest_name)
        if self.entity_fetcher is None and not self.id and not self.module.check_mode:
            self.module.fail_json(
                msg='Unable to find a fetcher for entity, and no ID specified. This is only supported if the root object can be a parent')

    def find_all(self):
        search_filter = ''

        if self.id:
            found_entity = self.entity_class(id=self.id)
            try:
                found_entity.fetch()
            except BambouHTTPError, e:
                self.module.fail_json(msg='Failed to fetch the specified entity by ID: {0}'.format(e))

            return [found_entity]

        elif self.properties:
            # Building filter
            for num, property_name in enumerate(self.properties):
                if num > 0:
                    search_filter += ' and '
                search_filter += '{0:s} == "{1}"'.format(property_name, self.properties[property_name])

        if self.entity_fetcher is not None:
            try:
                return self.entity_fetcher.get(filter=search_filter)
            except BambouHTTPError:
                pass
        return []

    def find_first(self):
        """
        Finds a single matching entity that matches all the provided properties, unless an ID is specified, in which
        case it just fetches the one item
        """
        search_filter = ''
        if self.id:
            found_entity = self.entity_class(id=self.id)
            try:
                found_entity.fetch()
            except BambouHTTPError, e:
                self.module.fail_json(msg='Failed to fetch the specified entity by ID: {0}'.format(e))

            return found_entity

        elif self.properties:
            # Building filter
            for num, property_name in enumerate(self.properties):
                if num > 0:
                    search_filter += ' and '
                search_filter += '{0:s} == "{1}"'.format(property_name, self.properties[property_name])

        if self.entity_fetcher is not None:
            try:
                return self.entity_fetcher.get_first(filter=search_filter)
            except BambouHTTPError:
                pass
        return None

    def handle_entity(self):
        if self.find and self.find == 'one':
            # Find state
            self.entity = self.find_first()
            self.result['changed'] = False
            if self.entity:
                self.result['id'] = self.entity.id
                self.result['entities'] = [self.entity.to_dict()]
            elif not self.module.check_mode:
                self.module.fail_json(msg='Unable to find a matching entity')
        elif self.find and self.find == 'all':
            # Find All state
            entities = self.find_all()
            self.result['changed'] = False
            if entities:
                for entity in entities:
                    self.result['entities'].append(entity.to_dict())
            elif not self.module.check_mode:
                self.module.fail_json(msg='Unable to find matching entries')
        elif self.state == 'present':
            # Present state
            self.entity = self.find_first()

            # Determining action to take
            if self.entity_fetcher is not None and self.entity_fetcher.relationship == 'member' and not self.entity:
                self.module.fail_json('Trying to assign an entity that does not exist')
            elif self.entity_fetcher is not None and self.entity_fetcher.relationship == 'member' and self.entity:
                # Entity is a member, need to check if already present
                if not self.is_member():
                    # Entity is not a member yet
                    if self.module.check_mode:
                        self.result['changed'] = True
                    else:
                        self.assign_member()
            elif self.entity_fetcher is not None and self.entity_fetcher.relationship in ['child',
                                                                                          'root'] and not self.entity:
                # Entity is not present as a child, creating
                if self.module.check_mode:
                    self.result['changed'] = True
                else:
                    self.create_entity()
            elif self.entity:
                # Need to compare properties in entity and found entity
                changed = False
                if self.properties:
                    for property_name in self.properties.keys():
                        entity_value = ''
                        try:
                            entity_value = getattr(self.entity, property_name)
                        except AttributeError:
                            self.module.fail_json(
                                msg='Property {0:s} is not valid for this type of entity'.format(property_name))

                        if entity_value != self.properties[property_name]:
                            # Difference in values changing property
                            changed = True
                            try:
                                setattr(self.entity, property_name, self.properties[property_name])
                            except AttributeError:
                                self.module.fail_json(
                                    msg='Property {0:s} can not be changed for this type of entity'.format(
                                        property_name))

                if self.module.check_mode:
                    self.result['changed'] = changed
                elif changed:
                    self.save_entity()
                else:
                    self.result['id'] = self.entity.id
                    self.result['entities'].append(self.entity.to_dict())
            elif not self.module.check_mode:
                self.module.fail_json(msg='Invalid situation, verify parameters')

        elif self.state == 'absent':
            # Absent state
            self.entity = self.find_first()
            if self.entity and (self.entity_fetcher is None or self.entity_fetcher.relationship in ['child', 'root']):
                # Entity is present, deleting
                if self.module.check_mode:
                    self.result['changed'] = True
                else:
                    self.delete_entity()
            elif self.entity and self.entity_fetcher.relationship == 'member':
                # Entity is a member, need to check if already present
                if self.is_member():
                    # Entity is not a member yet
                    if self.module.check_mode:
                        self.result['changed'] = True
                    else:
                        self.unassign_member()

        self.module.exit_json(**self.result)

    def is_member(self):
        """
        Verifies if the entity is a member of the parent in the fetcher
        """
        members = self.entity_fetcher.get()
        for member in members:
            if member.id == self.entity.id:
                return True
        return False

    def assign_member(self):
        """
        Adds the entity as a member to a parent
        """
        members = self.entity_fetcher.get()
        members.append(self.entity)
        try:
            self.parent.assign(members, self.entity_class)
        except BambouHTTPError, e:
            self.module.fail_json(msg='Unable to assign entity as a member: {0}'.format(e))
        self.result['changed'] = True
        self.result['id'] = self.entity.id
        self.result['entities'] = [self.entity.to_dict()]

    def unassign_member(self):
        """
        Removes the entity as a member of a parent
        """
        members = []
        for member in self.entity_fetcher.get():
            if member.id != self.entity.id:
                members.append(member)
        try:
            self.parent.assign(members, self.entity_class)
        except BambouHTTPError, e:
            self.module.fail_json(msg='Unable to remove entity as a member: {0}'.format(e))
        self.result['changed'] = True
        self.result['id'] = self.entity.id
        self.result['entities'] = [self.entity.to_dict()]

    def create_entity(self):
        """
        Creates a new entity in the parent, with all properties configured as in the file
        """
        self.entity = self.entity_class(**self.properties)
        try:
            self.parent.create_child(self.entity)
        except BambouHTTPError, e:
            self.module.fail_json(msg='Unable to create entity: {0}'.format(e))
        self.result['changed'] = True
        self.result['id'] = self.entity.id
        self.result['entities'] = [self.entity.to_dict()]

    def save_entity(self):
        """
        Updates an existing entity
        """
        try:
            self.entity.save()
        except BambouHTTPError, e:
            self.module.fail_json(msg='Unable to update entity: {0}'.format(e))
        self.result['changed'] = True
        self.result['id'] = self.entity.id
        self.result['entities'] = [self.entity.to_dict()]

    def delete_entity(self):
        """
        Deletes an entity
        """
        try:
            self.entity.delete()
        except BambouHTTPError, e:
            self.module.fail_json(msg='Unable to delete entity: {0}'.format(e))
        self.result['id'] = None
        self.result['changed'] = True


from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_username=dict(required=True, type='str', no_log=True),
            api_password=dict(required=True, type='str', no_log=True),
            api_enterprise=dict(required=True, type='str', no_log=True),
            api_url=dict(required=True, type='str'),
            type=dict(required=True, type='str'),
            id=dict(required=False, type='str'),
            parent_id=dict(required=False, type='str'),
            parent_type=dict(required=False, type='str'),
            state=dict(choices=['present', 'absent'], type='str'),
            find=dict(choices=['one', 'all'], type='str'),
            properties=dict(required=False, type='dict')
        ),
        supports_check_mode=True
    )

    if not HASVSPK:
        module.fail_json(msg='vspk is required for this module')

    entity_manager = NuageEntityManager(module)
    entity_manager.handle_entity()


if __name__ == '__main__':
    main()