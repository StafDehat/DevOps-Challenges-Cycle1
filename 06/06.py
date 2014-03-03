#!/usr/bin/env python

# Challenge 6: 
# Write a script that enables and executes a backup for a Cloud Database. 
# Pre-requisite is that the Cloud DB Instance must already exist with a valid 
# database (with some data) and a username with access to the DB. The user 
# executing the script should be able to choose the Instance, Database, and 
# User via the command line arguments to execute the backup. Choose your 
# language and SDK! 


# Instance, Database, User, Password?

import sys
import getopt
import uuid
import time
import pprint
import argparse
import time
from auth import *

CDB = pyrax.cloud_databases


parser = argparse.ArgumentParser(description='Backup a CDB database:')
parser.add_argument('-i','--instance', help='CDB Instance',required=True)
parser.add_argument('-d','--database',help='CDB Database', required=True)
parser.add_argument('-u','--user',help='CDB User with access to database', required=True)
args = parser.parse_args()
 
## show values ##
print ("Instance: %s" % args.instance )
print ("Database: %s" % args.database )
print ("User:     %s\n" % args.user )

#
# Ensure CDB instance exists
exists = False
cdbs = CDB.list()
for cdb in cdbs:
  if cdb.name == args.instance:
    print "CDB instance '" + cdb.name.rstrip() + "' exists\n"
    exists = True
    break
  #fi 
#done
if not exists:
  print "CDB instance '" + args.instance + "' does not exist\n"
  sys.exit()
#fi


#
# Ensure named database exists
# Nevermind, we don't need the database.


#
# Ensure named user exists
# Nevermind, we don't need the user.


print "Thanks for providing a database and user, but I'm gonna disregard that info.\n"
backupname=args.instance + "." + time.strftime("%F.%T")
print "Creating backup of instance '" + args.instance + "' named '" + backupname + "'"
cdb.create_backup(backupname)
print "That'll be done soon, thanks.\n"

