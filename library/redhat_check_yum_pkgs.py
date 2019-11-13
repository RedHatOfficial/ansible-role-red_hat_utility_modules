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
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}
 
DOCUMENTATION = '''
---
module: redhat_check_rpms
version_added: historical
short_description: Checks a list of RPMs against a target systems RPMs
 
description:
     - Checks a list of RPMs against a target systems RPMs
 
options:
 
# informational: requirements for nodes
author:
    - "Red Hat Consulting (NAPS)"
    - "Lester Claudio"
'''
 
EXAMPLES = '''
  - name: Check RPMs
    redhat_check_yum_pkgs:
      pkgs: ['iwl1000','pygpgme','iwl3160','yum','python-chardet','setools-libs','ncurses-libs','libcgroup']
      state: present
    resgister: response
 
  - debug: var=response
 
'''


import os
import sys
import yum
import json

class CheckYumPkgs:
  """
  A class used to check for system RPMs using YUM

  ...

  Attributes
  ----------
  all_installed_pkgs : dict
      An in-memory dictionary that contains all the installed packages available in the YUM DB
  tempjson : dict
      A temporary dictionary that will be returned with the values of the RPMs being 
      queried plus the state (present, absent).  This will be returned to Ansible.
  yb : YumBase()
      YumBase instance for the RPM python module

  #Methods
  #-------
  __init__ (self) 
      Constructor 

  check_pkg (self, item)
      Checks the RPM package against the all_installed_pkgs dictionary.  
      Returns: 'present' or 'absent'

  redhat_check_pkgs (self, pkgs, state)
      Takes the RPM package set, checks each one against the in-memory set
      and checks it against the state desired (installed or absent)

      Returns: rc and tempjson

  """

  def __init__(self):
    ## The transaction set will open the RPM database as needed, so in most cases, you do not need to explicitly open the database. The transaction set is the workhorse of RPM.
    self.yb = yum.YumBase()
    self.yb.setCacheDir()

    ## Dictionary with all the installed RPM names
    self.all_installed_pkgs = {}

    # Temporary dictionary which will be returned to Ansible once populated
    self.tempjson = {}
    # This takes the longest time for some reason.
    self.all_installed_packages = self.yb.doPackageLists(pkgnarrow='installed', patterns=None, showdups=None, ignore_case=False, repoid=None)
    ## Let's build a in-memory dictionary with all the RPMs in the system
    for h in self.all_installed_packages:
        #rpmname="%s-%s-%s.%s" % (h['name'], h['version'], h['release'], h['arch'])    
        #rpmname="%s" % (h['name'])    
        #print ("RPMNAME: %s\n", rpmname)
        self.all_installed_pkgs[h['name']] = 'installed'


  def check_pkg( self, item ):
     try:
       ## Now we check if the item is in the in-memory dictionary
       if item in self.all_installed_pkgs:
         return 'present'
     except:
       return 'absent'
   
  def redhat_check_pkgs( self, pkgs, state ):
     rc = 0
   
     for item in pkgs:
        #print ("Checking %s \n" % item)
        found = self.check_pkg ( item )
        if found == state:
           self.tempjson[ item ] = 'present'
        else:
           self.tempjson[ item ] = 'absent'
           rc += 1         
     return rc,self.tempjson 

def main():
 
    module = AnsibleModule(
        argument_spec = dict(
           pkgs = dict(required = True, type='list'),
           state = dict(default='present', choices=['present', 'absent'])
        ),
        supports_check_mode = True
    )
 
    params = module.params
 
    pkgs = params.get('pkgs', '')
    state = params.get('state', '')
 
    checkPkgs = CheckYumPkgs()
    rc,pkgstat = checkPkgs.redhat_check_pkgs( pkgs, state )

    tempjson={}
    if rc == 0:
       if not pkgstat:
           failmsg="Empty set"
           module.fail_json(msg=failmsg)
       else:
           tempjson['pkgstat']=pkgstat
           module.exit_json(**tempjson)
    else:
       failmsg="Number of Packages that are non compliant: [%d]" % rc
       tempjson['pkgstat']=pkgstat
       tempjson['failmsg']=failmsg
       module.exit_json(rc=rc, **tempjson)
 
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()


