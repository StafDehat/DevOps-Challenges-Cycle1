#!/usr/bin/env python

#  Challenge 5:
# Write a script that creates a Cloud Database. If a CDB already exists with
# that name, suggest a new name like "name1" and give the user the choice to
# proceed or exit. The script should also create X number of Databases and X 
# number of users in the new Cloud Database Instance. The script must return 
# the Cloud DB URL. Choose your language and SDK!


from auth import *

cdb = pyrax.cloud_databases




