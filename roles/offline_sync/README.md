# galaxy.galaxy.offline_sync

## Description

An Ansible Role to offline_sync collections to Automation Hub or Galaxies.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|no|Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`ah_configuration_working_dir`|`/var/tmp/pah_offline_sync`|no|The working directory where the collections will be downloaded and any required files.||

## Data Structure

### ah_collections Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`collection_name`|""|yes|str|Name of collection, normally the last part before the / in a git url.|
|`git_url`|""|no|str|Url to git repo. Required if collection_local_path not set|
|`version`|""|no|str|Git ref to pull. Will default to default branch if unset. Can specify tag, branch or commit ref here.|
|`key_path`|""|no|str|Path to ssh key for authentication.|
|`ssh_opts`|""|no|str|Options git will pass to ssh when used as protocol.|
|`collection_local_path`|""|no|str|Path to collection stored locally. Required if git_url not set. This value will be used rather than git_url if set.|

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Download all collections from Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ah_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  # ah_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - galaxy.galaxy.offline_sync
```

### Playbook to upload to offline Automation Hub after using this role to download the collections.

```yaml
---
- name: Upload all collections
  hosts: localhost
  gather_facts: false
  connection: local
  vars_files:
    - "collections.yml"
  pre_tasks:
    - name: Include vars from ah_configs directory with collections.yml file added
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  tasks:
    - name: Ensure the namespaces exists
      ansible.builtin.import_role:
        name: galaxy.galaxy.namespace

    - name: Upload collections
      ansible.builtin.include_role:
        name: galaxy.galaxy.collection
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)

## Author

[David Danielsson](https://github.com/djdanielsson)
