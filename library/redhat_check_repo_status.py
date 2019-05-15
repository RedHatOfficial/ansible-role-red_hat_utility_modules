#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# (c) 2012, Red Hat, Inc
# Based on yum module written by Seth Vidal <skvidal at fedoraproject.org>
# (c) 2014, Epic Games, Inc.
# Written by Lester Claudio <claudiol at redhat.com>
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
#
 
import os
import platform
import tempfile
import shutil
import ConfigParser
import json 
 
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}
 
DOCUMENTATION = '''
---
module: redhat_check_repo_status
version_added: historical
short_description: Checks status for subscription manager repository information
 
description:
     - Checks status for subscription manager identity information
 
options:
 
# informational: requirements for nodes
author:
    - "Red Hat Consulting (NAPS)"
    - "Lester Claudio"
'''
 
EXAMPLES = '''
  - name: Checking Repositories are enabled
    redhat_check_repo_status:
      repos: ['rhel-7-server-extras-rpms']
      status: 1
    register: response

  - name: Debug
    debug:
      var: response
 
'''
 
def check_repo( repo, config, status ):
   try:
      current_state = config.get(repo, "enabled")
      
      if ( status == current_state ):
         return current_state
      else:
         return current_state
   except ConfigParser.NoSectionError as e:
      return -1
   
def redhat_check_repo_status( repos, status, repofile ):
   rc = 0
   config = ConfigParser.ConfigParser()
   config.read(repofile)
   
   tempjson = {}
   
   for repo in repos:
      enabled = check_repo ( repo, config, status )
      if enabled < 0:
         tempjson[ repo ] = "Repository not entitled by current subscription"
         rc = 1
      elif status == enabled:
         tempjson[ repo ] = enabled
      else:
         tempjson[ repo ] = enabled
         

   return rc,tempjson 
      


  
def main():
 
    module = AnsibleModule(
        argument_spec = dict(
           repos = dict(required = True, type='list'),
           repofile = dict(required = False, default="/etc/yum.repos.d/redhat.repo"),
           status = dict(required=True, type="bool")
        ),
        supports_check_mode = True
    )
 
    params = module.params
 
    repos = params.get('repos', '')
    repofile = params.get('repofile', '')
    status = params.get('status', '')
 
    exists = os. path. isfile(repofile)

    if (exists):
      rc,repostat = redhat_check_repo_status( repos, status, repofile )
    else:
       rc = 1
       failmsg="Errors occurred! File [%s] does not exist!" % repofile
      

    tempjson={}
    if rc == 0:
       repostat['rc'] = rc
       tempjson["repostat"]=repostat
       module.exit_json(**tempjson)
    else:
       repostat['rc'] = rc
       tempjson['repostat']=repostat
       tempjson['failmsg']=failmsg
       module.exit_json(rc=rc, **tempjson)
 
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
