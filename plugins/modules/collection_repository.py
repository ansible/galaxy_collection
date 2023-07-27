#!/usr/bin/python
# coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = """
---
module: collection_repository
author: "tbd"
short_description: Create, Update, Delete repository.
description:
    - Configure an Automation Hub repository. See
      U(https://www.ansible.com/) for an overview.
options:
    state:
      description:
        - If C(absent), then the module deletes the repository and its distribution.
        - If C(present), then the module updates the repository.
      type: str
      choices: ["present", "absent"]
      default: present
    name:
      description:
        - Repository name.
      required: True
      type: str
    description:
      description:
        - Description for the repository.
      required: False
      type: str
    pulp_labels:
      description: An Ansible Fact variable representing a Tower token object which can be used for auth in subsequent modules. See examples for usage.
      contains:
        pipeline:
          description: Pipeline adds repository labels with pre-defined meanings.
          type: str
          choices: [None, "approved", "staging", "rejected"]
        hide_from_search:
          description: Prevent collections in this repository from showing up on the home page.
          type: str
    distribution:
      description:
        - Content in repositories without a distribution will not be visible to clients for sync, download or search.
      contains:
        name:
          description: 
            - Distribution name and base_path.
            - If not set, repository name is used.
          type: str
        state:
          description: 
            - If C(absent), then the module deletes the distribution.
            - If C(present), then the module creates or updates the distribution.
          type: str
          choices: ["present", "absent"]
    private:
      description:
        - Make the repository private.
      type: str
      default: False
    remote:
      description:
        - Existing remote name.
      type: str

extends_documentation_fragment: ansible.automation_hub.auth
"""


EXAMPLES = """
- name: Create "foobar" repository with distribution and remote
  ansible.automation_hub.collection_repository:
    state: present
    name: "foobar"
    description: "description of foobar repository"
    pulp_labels:
      pipeline: "approved"
    distribution:
      name: "foobar"
      state: present
    remote: community

- name: Create rejected "foobar" repository with
  ansible.automation_hub.collection_repository:
    state: present
    name: "foobar"
    description: "description of foobar repository"
    pulp_labels:
      pipeline: "rejected"
      hide_from_search: ""

- name: Delete "foobar" repository
  ansible.automation_hub.collection_repository:
    state: absent
    name: "foobar"
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_pulp_object import (
  AHPulpAnsibleRepository,
  AHPulpAnsibleDistribution,
  AHPulpAnsibleRemote
)


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        description=dict(),
        retain_repo_versions=dict(type="int", default=1),
        distribution=dict(type="dict"),
        pulp_labels=dict(type="dict"),
        private=dict(type="bool", default=False),
        remote=dict(),
        state=dict(choices=["present", "absent"], default="present"),
    )

    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    module.fail_on_missing_params(["name"])
    new_fields = {}
    repo_fields = {}

    # Authenticate
    module.authenticate()

    repo_keys = [
      "name",
      "description",
      "retain_repo_versions",
      "pulp_labels",
      "private",
      "remote"
    ]

    for field_name in (
        *repo_keys,
        "distribution",
        "state"
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
          new_fields[field_name] = field_val
          
          if field_name in repo_keys:
            repo_fields[field_name] = field_val

    ansible_repository = AHPulpAnsibleRepository(module)
    ansible_repository.get_object(name=name)

    if distro := new_fields.get("distribution"):
      # if "distribution" is set, but "state" is missing, set "present"
      distro_state = distro.get("state", None)

      if distro_state not in [None, "present", "absent"]:
        module.fail_json(
          msg="value of state must be one of: present, absent, got: {}".format(distro_state)
        )

      if not distro_state:
        distro_state = "present"

      # if distro name isn't specified, use repo name as distro
      distro_name = distro.get("name", None)
      if not distro_name:
        distro_name = name

      ansible_distro = AHPulpAnsibleDistribution(module)
      ansible_distro.get_object(name=distro_name)


    if new_fields.get("state") == "absent":
      if distro:
        ansible_distro.delete(auto_exit=False)

      ansible_repository.delete(auto_exit=True)


    if remote := new_fields.get("remote"):
      ansible_remote = AHPulpAnsibleRemote(module)
      ansible_remote.get_object(name=remote)

      if not ansible_remote.exists:
        module.fail_json(msg="Remote {0} doesn\'t exist.".format(remote))

      repo_fields["remote"] = ansible_remote.data.get("pulp_href")
    else:
      repo_fields["remote"] = None

    if ansible_repository.exists:
      ansible_repository.update(
        new_item=repo_fields,
        auto_exit=False
      )
    else:
      ansible_repository.create(
        new_item=repo_fields,
        auto_exit=False
      )

    repo_href = ansible_repository.data.get('pulp_href')

    if distro:
      if not ansible_distro.exists:
        if distro_state == "present":
          ansible_distro.create(
            new_item={
              "base_path": distro_name,
              "name": distro_name,
              "repository": repo_href
            },
            auto_exit=False
          )
      else:
        if distro_state == "absent":
          ansible_distro.delete(auto_exit=False)
        elif distro_state == "present":
          ansible_distro.update(
            new_item={
              "base_path": distro_name,
              "repository": repo_href
            },
            auto_exit=False
          )

    json_output = {
        "name": name,
        "type": ansible_repository.object_type,
        "changed": True,
    }
    module.exit_json(**json_output)


if __name__ == "__main__":
    main()
