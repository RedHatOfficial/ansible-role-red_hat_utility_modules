# ansible-role-red_hat_utility_modules
An Ansible role that contains re-useable miscellaneous utility modules for various Red Hat tools and products.

These are modules that are not currently shipped with Ansible but others may find useful. They are distributed in a role for easier consumption so the user does not need to copy paste the module files into their own repositories and rather can do a dynamic role requirement to pull in these modules.

## Modules

### redhat_check_rpms.py

This module checks a list of RPMs against a target systems RPMs. The idea is that using this module you can 
verify if a set of RPMs either exists or are absent from a target system.  Some of our customers use this 
to ensure that a system, after it has been provisioned, contains the exact RPM set that was expected. 
 
EXAMPLES:
  - name: Check RPMs are present
    redhat_check_rpms:
      rpms: ['iwl1000-firmware-39.31.5.1-69.el7.noarch','pygpgme-0.3-9.el7.x86_64','iwl3160-firmware-22.0.7.0-69.el7.noarch','yum-rhn-plugin-2.0.1-10.el7.noarch','python-chardet-2.2.1-1.el7_1.noarch','setools-libs-3.3.8-4.el7.x86_64','ncurses-libs-5.9-14.20130511.el7_4.x86_64','libcgroup-0.41-20.el7.x86_64']
      state: present
    register: response
 
  - debug: var=response
 
  - name: Check that RPMs are absent
    redhat_check_rpms:
      rpms: ['iwl1000-firmware-39.31.5.1-69.el7.noarch','pygpgme-0.3-9.el7.x86_64','iwl3160-firmware-22.0.7.0-69.el7.noarch','yum-rhn-plugin-2.0.1-10.el7.noarch','python-chardet-2.2.1-1.el7_1.noarch','setools-libs-3.3.8-4.el7.x86_64','ncurses-libs-5.9-14.20130511.el7_4.x86_64','libcgroup-0.41-20.el7.x86_64']
      state: absent
    register: response
 
  - debug: var=response

### redhat_check_repo_status.py

This module checks that the repositories on a target system are either enabled or disabled. The idea is that using 
this module you can verify the repositories that are enabled without having to run subscription-manager on each
target system.  This module checks the "redhat.repo" file in the /etc/yum.repos.d directory by default but a
different repo file can be speficied using the repofile: argument.
 
EXAMPLES:

  - name: Checking Repositories are enabled
    redhat_check_repo_status:
      repos: ['rhel-7-server-extras-rpms']
      status: 1
    register: response

  - name: Debug
    debug:
      var: response.repostat

  - name: Checking Repositories are enabled
    redhat_check_repo_status:
      repos: ['rhel-7-server-extras-rpms']
      repofile: /etc/yum.repos.d/myrepofile.repo
      status: 1
    register: response

  - name: Debug
    debug:
      var: response.repostat
