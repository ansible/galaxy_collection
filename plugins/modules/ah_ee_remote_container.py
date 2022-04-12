#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
<<<<<<< HEAD
module: ah_ee_remote_container
=======
module: ah_namespace
>>>>>>> e86bf25cf4d7f072385eb2c26a12a420c8bee84d
author: "Sean Sullivan (@sean-m-sullivan)"
short_description: create, update, or destroy Automation Hub Namespace.
description:
    - Create, update, or destroy Automation Hub Namespace. See
      U(https://www.ansible.com/) for an overview.
options:
    name:
      description:
        - Namespace name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str

extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""


EXAMPLES = """

"""

from ..module_utils.ah_module import AHModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        description=dict(),
        company=dict(),
        email=dict(),
        avatar_url=dict(),
        resources=dict(),
        links=dict(type="list", elements="dict"),
        groups=dict(type="list", elements="dict"),
        state=dict(choices=["present", "absent"], default="present"),
    )


    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="namespaces",
        item_type="namespaces",
    )


if __name__ == "__main__":
    main()
