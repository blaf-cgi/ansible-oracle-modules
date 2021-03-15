#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Ari Stark <ari.stark@netcourrier.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
module: oracle_quota
short_description: Manages Oracle quota for users.
description:
    - This module manages Oracle quota for users.
    - It can ensure a single quota is present/absent.
    - It can ensure a list of quotas matches the quotas in database.
    - It can ensure a user has no quota.
version_added: "1.2.0"
author:
    - Ari Stark (@ari-stark)
options:
    hostname:
        description:
            - Specify the host name or IP address of the database server computer.
        default: localhost
        type: str
    mode:
        description:
            - This option is the database administration privileges.
        default: normal
        type: str
        choices: ['normal', 'sysdba']
    oracle_home:
        description:
            - Define the directory into which all Oracle software is installed.
            - Define ORACLE_HOME environment variable if set.
        type: str
    password:
        description:
            - Set the password to use to connect the database server.
            - Must not be set if using Oracle wallet.
        type: str
    port:
        description:
            - Specify the listening port on the database server.
        default: 1521
        type: int
    schema_name:
        description:
            - Name of the user to manage.
        required: true
        type: str
        aliases:
            - name
    service_name:
        description:
            - Specify the service name of the database you want to access.
        required: true
        type: str
    size:
        description:
            - Specify the size of the quota.
        default: unlimited
        type: str
    state:
        description:
            - Specify the state of the quota.
            - If I(state=absent) and no I(tablespace) nor I(tablespaces) are defined, all quotas will be removed.
            - If I(state=absent) with I(tablespace) or I(tablespaces), quotas will be remove for these tablepaces.
        default: present
        type: str
        choices: ['absent', 'present']
    tablespace:
        description:
            - Specify the tablespace name where quota must be defined.
            - I(tablespace) and I(tablespaces) are mutually exclusive.
            - When defined, module ensures the defined quota is absent/present with defined size.
        required: false
        type: str
    tablespaces:
        description:
            - Specify the list of tablespaces names where quota must be defined.
            - I(tablespace) and I(tablespaces) are mutually exclusive.
            - When defined and I(state=present), modules ensures the quotas are defined exactly,
              removing or adding quotas.
            - When defined and I(state=absent), modules ensures the quotas are absent for these tablespaces.
        required: false
        type: list
        elements: str
    username:
        description:
            - Set the login to use to connect the database server.
            - Must not be set if using Oracle wallet.
        type: str
        aliases:
            - user
requirements:
    - Python module cx_Oracle
    - Oracle basic tools.
notes:
    - Check mode and diff mode are supported.
'''

EXAMPLES = '''
- name: define unlimited quota to user on a tablespace
  oracle_quota:
    service_name: "xepdb1"
    username: "sys"
    password: "manager"
    mode: "sysdba"
    schema_name: "foo_user"
    tablespace: "foo_ts"
    state: "present"

- name: define quota to user on a tablespace
  oracle_quota:
    service_name: "xepdb1"
    username: "sys"
    password: "manager"
    mode: "sysdba"
    schema_name: "foo_user"
    tablespace: "foo_ts"
    size: "5M"
    state: "present"

- name: ensure quota for a user are defined (add, remove or change quota)
  oracle_quota:
    service_name: "xepdb1"
    username: "sys"
    password: "manager"
    mode: "sysdba"
    schema_name: "foo_user"
    tablespaces:
      - "foo_ts"
      - "bar_ts"
    size: "5M"
    state: "present"

- name: ensure quota is absent for user on a tablespace
  oracle_quota:
    service_name: "xepdb1"
    username: "sys"
    password: "manager"
    mode: "sysdba"
    schema_name: "foo_user"
    tablespace: "foo_ts"
    state: "absent"

- name: ensure a user has no quota
  oracle_quota:
    service_name: "xepdb1"
    username: "sys"
    password: "manager"
    mode: "sysdba"
    schema_name: "foo_user"
    state: "absent"
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ari_stark.ansible_oracle_modules.plugins.module_utils.ora_db import OraDB


def main():
    global module
    global ora_db

    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(type='str', default='localhost'),
            mode=dict(type='str', default='normal', choices=['normal', 'sysdba']),
            oracle_home=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            port=dict(type='int', default=1521),
            schema_name=dict(type='str', required=True, aliases=['name']),
            service_name=dict(type='str', required=True),
            size=dict(type='str', default='unlimited'),
            state=dict(type='str', default='present', choices=['absent', 'present']),
            tablespace=dict(type='str', required=False),
            tablespaces=dict(type='list', elements='str', required=False),
            username=dict(type='str', required=False, aliases=['user']),
        ),
        required_together=[['username', 'password']],
        mutually_exclusive=[['tablespace', 'tablespaces']],
        supports_check_mode=True,
    )

    schema_name = module.params['schema_name']
    size = module.params['size']
    state = module.params['state']
    tablespace = module.params['tablespace']
    tablespaces = module.params['tablespaces']

    ora_db = OraDB(module)

    module.exit_json(msg="Nothing was done.", changed=False)


if __name__ == '__main__':
    main()
