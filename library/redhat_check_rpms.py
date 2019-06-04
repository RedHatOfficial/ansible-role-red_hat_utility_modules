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
import rpm
 
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
    redhat_check_rpms:
      rpms: ['iwl1000-firmware-39.31.5.1-69.el7.noarch','pygpgme-0.3-9.el7.x86_64','iwl3160-firmware-22.0.7.0-69.el7.noarch','yum-rhn-plugin-2.0.1-10.el7.noarch','python-chardet-2.2.1-1.el7_1.noarch','setools-libs-3.3.8-4.el7.x86_64','ncurses-libs-5.9-14.20130511.el7_4.x86_64','libcgroup-0.41-20.el7.x86_64']
      state: present
    resgister: response
 
  - debug: var=response
 
'''


class CheckRPMS:
  """
  A class used to check for system RPMs

  ...

  Attributes
  ----------
  all_rpms : dict
      An in-memory dictionary that contains all the RPMs available in the RPM DB
  tempjson : dict
      A temporary dictionary that will be returned with the values of the RPMs being 
      queried plus the state (present, absent).  This will be returned to Ansible.
  ts : rpm.TransactionSet()
      TransactionSet for the RPM python module
  mi : Iterator
      Iterator for the RPM in the RPM DB

  Methods
  -------
  __init__ (self) 
      Constructor 

  check_rpm (self, item)
      Checks the RPM against the all_rpms dictionary.  
      Returns: 'present' or 'absent'

  redhat_check_rpms (self, rpms, state)
      Takes the RPM set, checks each one against the in-memory set
      and checks it against the state desired (present or absent)

      Returns: rc and tempjson

  """

  def __init__(self):
    # The transaction set will open the RPM database as needed, so in most cases, you do not need to explicitly open the database. The transaction set is the workhorse of RPM.
    self.ts = rpm.TransactionSet()
 
    # Now let's get the iterator
    self.mi = self.ts.dbMatch()

    # Dictionary with all the RPM names
    self.all_rpms = {}

    # Temporary dictionary which will be returned to Ansible once populated
    self.tempjson = {}

    # Let's build a in-memory dictionary with all the RPMs in the system
    for h in self.mi:
        rpmname="%s-%s-%s.%s" % (h['name'], h['version'], h['release'], h['arch'])    
        self.all_rpms[rpmname] = 'present'


  def check_rpm( self, item ):
     try:
       # Now we check if the item is in the in-memory dictionary
       if self.all_rpms[item]:
         return 'present'
     except:
       return 'absent'
   
  def redhat_check_rpms( self, rpms, state ):
     rc = 0
   
     for item in rpms:
        found = self.check_rpm ( item )
        if found == state:
           self.tempjson[ item ] = 'present'
        else:
           self.tempjson[ item ] = 'absent'
           rc += 1         

     return rc,self.tempjson 
      
def main():
 
    module = AnsibleModule(
        argument_spec = dict(
           rpms = dict(required = True, type='list'),
           state = dict(default='present', choices=['present', 'absent'])
        ),
        supports_check_mode = True
    )
 
    params = module.params
 
    rpms = params.get('rpms', '')
    state = params.get('state', '')
 
    checkRpms = CheckRPMS()
    rc,rpmstat = checkRpms.redhat_check_rpms( rpms, state )

    tempjson={}
    if rc == 0:
       if not rpmstat:
           failmsg="Empty set"
           module.fail_json(msg=failmsg)
       else:
           tempjson['rpmstat']=rpmstat
           module.exit_json(**tempjson)
    else:
       failmsg="Number of RPMs that are non compliant: [%d]" % rc
       tempjson['rpmstat']=rpmstat
       tempjson['failmsg']=failmsg
       module.exit_json(rc=rc, **tempjson)
 
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
