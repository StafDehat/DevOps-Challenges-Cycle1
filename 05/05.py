#!/usr/bin/env python

# Challenge 5:
# Write a script that creates a Cloud Database. If a CDB already exists with
# that name, suggest a new name like "name1" and give the user the choice to
# proceed or exit. The script should also create X number of Databases and X 
# number of users in the new Cloud Database Instance. The script must return 
# the Cloud DB URL. Choose your language and SDK!

import uuid
from auth import *

CDB = pyrax.cloud_databases


cdbname = raw_input("Name of Cloud DataBase instance: ")
cdbs = CDB.list()
for cdb in cdbs:
  if cdb.name == cdbname:
    print cdb.name.rstrip(), "exists\n"
    opt = raw_input("Try " + str(uuid.uuid1()) + " instead? [Y/n] ");





