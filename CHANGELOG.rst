====================================
infra.ah_configuration Release Notes
====================================

.. contents:: Topics


v2.0.4
======

Bugfixes
--------

- Removed References in the readmes to token authentication for any module that does not support token authentication.
- Removed token authentication from the following roles - collection_remote, collection_repository, collection_repository_sync. The corresponding modules did not support token authentication.
- ah_repository_sync incorrectly stated which module replaced it, It is being replaced by collection_repository_sync.

v2.0.0
======

Major Changes
-------------

- Added collection_remote role and module to manage collection remotes. This will only work in Galaxy 4.7 or AAP 2.4.
- Added collection_repository and collection_repository_sync roles and modules to manage collection repositories. This will only work in Galaxy 4.7 or AAP 2.4.
- Added group_roles role and module to manage and attach roles to groups. Global role assignment will only work in Galaxy 4.6 or AAP 2.3 or later, while the targeted role assignment will work in Galaxy 4.7 or AAP 2.4 and above.

Minor Changes
-------------

- Add arg spec to all roles
- Add option to change async directory, and set the default to null. /tmp/.ansible_async was a workaround while the default was broken previously.
- Add role option for proxy information rather than being forced to use global
- Added argument spec for ansible_config role
- Added auth_url option for automation_hub_list in ansible_config role
- Added request_timeout option for plugins and roles in the collection
- Changed ansible_config template to default to use ah_token and prevent two tokens being added
- In ansible_config role, changed default singular value of ansible_config_list to take the validate_certs from the ah_validate_certs value as documented
- Updated ah_groups module to use new Pulp endpoint. The change should be seamless.
- Updated output in multiple roles to provide more information.
- Updated server version lookup to remove the dev portion if working on a developmental version of Galaxy.
- added more permissions to the ah_role modules. Consult your web UI to see what roles are available specific to your version.
- added more roles to the dispatch role
- ansible.cfg removed from root and galaxy.yml added to enable install from source

Breaking Changes / Porting Guide
--------------------------------

- Update collection repository roles to use allow for lists (you now need to have a name for each repo and update the variable name) as this has been expanded in the newer version of the product.

Deprecated Features
-------------------

- Added warnings to ah_ee_namespace module to depreciate it and the ee_namespace role that they will be removed when support for AAP 2.2 ends in November of 2023.
- Added warnings to ah_group_perm module to depreciate it and the group role that uses it they will be removed when support for AAP 2.2 ends in November of 2023.
- Added warnings to ah_repository module to depreciate it and the repository role that they will be removed when support for AAP 2.3 ends in May of 2024.
- Added warnings to ah_repository_sync module to depreciate it and the repository_sync role that they will be removed when support for AAP 2.3 ends in May of 2024.
- ah_repository, ah_repository_sync modules and repository, repository_sync roles are being depreciated, they will be removed when support for AAP 2.3 ends in May of 2024.

Bugfixes
--------

- Fix issue where changing an execution environment repository caused an error statingCannot make a PUT request to this endpoint.
- Fixed a flake8 failure with comparison of types.
- Fixed documentation for ansible_config role
- Fixed role readme errors and standardised variable section of role readmes

New Modules
-----------

- infra.ah_configuration.group_roles - Add roles to private automation hub user groups

v1.1.1
======

Minor Changes
-------------

- Simplify dispatch role
- remove unused import module

Bugfixes
--------

- add ah_token for the community repository. This commit adds that.

v1.1.0
======

Minor Changes
-------------

- Added ansible role 'role' for creating roles of group permsions.
- Fixed issue with ah_ee_repository working on newer versions.
- Fixed issue with ah_namespace delete
- Updated ah_collection_upload to exit properly.
- Updated ah_role to not require permisions in order to allow for deletion.
- Updated testing coverage.
- add the ah_role module to add role permisions.
- added better error catching to ah_ee_registery_index/sync to handle when a registery is not found.
- ah_ee_repository include/exclude tags are no longer mutually exclusive
- updated UI get_object method to use version variable.
- updated ah_ee_image to work with galaxy 4.7+
- updated ah_ee_repository to work with galaxy 4.6+

Breaking Changes / Porting Guide
--------------------------------

- Introduces a `sync` option to the ee_registry_sync role on the `ah_ee_registries` variable which by default is false and which is required true to sync the registry.
- Introduces a `sync` option to the ee_repository_sync role on the `ah_ee_repositories` variable which by default is false and which is required true to sync the repository.
- Introduces an `index` option to the ee_registry_index role on the `ah_ee_registries` variable which by default is false and which is required true to index the registry.
- Removed ah_ee_registry new name option. This affected underlying images indexed from the registery leaving them abandoned, and subsequent indexes of the renamned registery would fail.
- removed the options of new_name and delete_namespace_if_empty from ah_ee_repository. This is due to limitations of the API that broke pushing images to old repository name.

New Modules
-----------

- infra.ah_configuration.ah_role - Manage a role of group permissions

v1.0.1
======

Minor Changes
-------------

- Added option to pull all collections from a specific repository
- Collection module and role - add way to get version from path for auto approval if not provided.
- Update Publish role to be namespace agnostic.

Bugfixes
--------

- Checks for username and password passed to api lookup plugin
- Removed incorrect reference to oauth token abilities for api lookup plugin.

v1.0.0
======

Minor Changes
-------------

- Added timeout and interval for waiting for auto approval on ah_collection module.
- Added timeout and interval for waiting for auto approval on collection role.
- Changed default of overwrite_existing var in collection role to False to match module
- groups option of ah_namespace module changed to accept just the names of groups who own the namespace

Bugfixes
--------

- Enforced type checking on groups option of ah_namespace
- Fixed doc issue in ah_collection module where overwrite_existing option was reported with default True when functionality was False
- Fixed doc issue in ah_collection_upload module where wait option was reported with default True when functionality was False
- Fixed doc issue in collection role where ah_overwrite_existing option was reported with default True when functionality was False
- Removed ah_token from roles where the modules don't accept it
- Secret fields (password, client_key, proxy_password) set to no_log in ah_ee_registry module
- Updated ah_ee_namespace to use object_roles instead of object_permissions when inspecting group permissions
- token option in ah_repository set as no_log to prevent exposure of secret
- url field explicitly required when state=present in ah_ee_registry module

v0.9.2
======

Minor Changes
-------------

- Add markdown linter
- Fix all linter reported errors
- Move linter configurations to root directory
- Update linter versions
- add `ah_token` so `repository_sync` that was missing
- created a role from ah_collection module

Deprecated Features
-------------------

- ah_token auth for modules

Bugfixes
--------

- Fixed a major bug that was preventing publish role from uploading new versions without removing all prior versions.

Known Issues
------------

- ah_overwrite_existing when set to true, will sometimes cause errors due to the time it takes to delete namespaces
- ah_token does not work in every module (errors saying parameter is not supported)
- auto_approve does not work when publishing new collections (throws error)

v0.9.1
======

Major Changes
-------------

- Adds the ah_api lookup plugin to do generic API lookups on endpoints.

v0.8.1
======

Major Changes
-------------

- Allows basic auth as backup method to enable keycloak based users to authenticate.

Minor Changes
-------------

- Added certificate and key authentication for ee registries in ah_ee_registry module
- Added repository role
- Added repository sync role
- Added several options to the ah_repository module

Bugfixes
--------

- Fixed an issue where a genuine API error would cause a module to have an unhandled error.
- Fixed incorrect task names on serveral roles
- Fixed issue where groups was required to create a namespace using ah_namespace module

v0.8.0
======

Minor Changes
-------------

- Changed default retries on async tasks in roles to 50

Bugfixes
--------

- Fix issue where all roles had the wrong variable set and caused failures
- Fixed issue with new variables not included in ee_repository role
- Fixed issue with sync and index roles where a no_log variable was incorrect

v0.7.0
======

Major Changes
-------------

- Added ability to add remote repositories in ah_ee_repository module.
- Adds ah_ee_registry module
- Adds ah_ee_registry_index module
- Adds ah_ee_registry_sync module
- Adds ee_registry role
- Adds ee_registry_index role
- Adds ee_registry_sync role
- module ah_collection can now upload and delete collections

Minor Changes
-------------

- Added group permissions for remote registry management - add_containerregistryremote, change_containerregistryremote, delete_containerregistryremote.
- ah_hostname becomes an alias for ah_host in modules
- ah_hostname is now the default option for roles, though ah_host remains an alias

Breaking Changes / Porting Guide
--------------------------------

- Options for state in ah_ee_image and ah_ee_repository modules changed from 'updated' to 'present' as a bug fix.
- module ah_collection_upload has been removed.

New Modules
-----------

- infra.ah_configuration.ah_ee_registry - Manage private automation hub execution environment remote registries.

v0.6.1
======

Minor Changes
-------------

- added namespace state absent module parameter
- added new permision options to the ah_group_perm module and group role.
- ah_ee_namespace and ah_ee_repository - adding the ``new_name`` parameter so that users can rename namespaces and repositories (https://github.com/redhat-cop/ah_configuration/issues/44)
- removed dependency for ansible.galaxy module which wasn't accessible in 2.12 Ansible

v0.5.5
======

Bugfixes
--------

- Add the `no_log` attribute to the `password` and `proxy_password` fields of the `ah_repository` module (Resolves

v0.5.0
======

Major Changes
-------------

- Added execution_environment plugins
- Added user, group and group_perm plugins

v0.4.3
======

Minor Changes
-------------

- Added meta/runtime.yml file which is now a requirement for collections to be released on Galaxy
- Added requirements_file option to ah_repository module

v0.4.1
======

Bugfixes
--------

- Now retries auto-approving on the publish role in case there is a delay in the collection making it to be ready for approval.

v0.4.0
======

Major Changes
-------------

- Added ah_repository_sync module to sync remote repositories for Automation Hub.

v0.3.1
======

Bugfixes
--------

- Fixes issue in ah_repository where not specifying a requirements list causedd a failure.

v0.3.0
======

Major Changes
-------------

- Added ah_repository module to configure the remote repositories for Automation Hub.

v0.2.0
======

Major Changes
-------------

- Added ah_approval module to approve a colelction which has been uploaded.
- Added ah_collection_uploads module
- Publish role - Ability to approve role added
- Publish role - rewritten to use internal modules

Breaking Changes / Porting Guide
--------------------------------

- Publish role - repo_name variable renamed to collection_name.

v0.1.0
======

Major Changes
-------------

- Initial release of ansible_config, namespace, publish roles and ah_namespace, ah_token modules
