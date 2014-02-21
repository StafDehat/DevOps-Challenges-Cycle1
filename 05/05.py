#!/usr/bin/env python

# Challenge 5:
# Write a script that creates a Cloud Database. If a CDB already exists with
# that name, suggest a new name like "name1" and give the user the choice to
# proceed or exit. The script should also create X number of Databases and X 
# number of users in the new Cloud Database Instance. The script must return 
# the Cloud DB URL. Choose your language and SDK!

# Python is a steaming pile.  Call me when you're ready to go PHP instead.
# (04:04:56 PM) Joe Stevenson: in > 2.6
# (04:04:50 PM) Joe Stevenson: apparently you can do "db{0}".format(x)
# (04:05:14 PM) Joe Stevenson: I don't know if thats better but it's definitely different


import uuid
import time
import pprint
from pprint import pprint
from inspect import getmembers
from auth import *

CDB = pyrax.cloud_databases

#
# Figure a name for the new instance
cdbname = raw_input("Desired name of Cloud DataBase instance: ")
cdbs = CDB.list()
for cdb in cdbs:
  if cdb.name == cdbname:
    print cdb.name.rstrip(), "exists\n"
    cdbname = str(uuid.uuid1())
    opt = raw_input("Use " + cdbname + " instead? [Y/n] ");
    if opt != "Y" and opt != "y":
      print "If that's how you're gonna be, we're done here.\n";
      exit(0)
    #fi
  #fi 
#done
print "Database name: '"+cdbname+"'"
print "So it is written.  So it shall be.\n"


#
# Prompt for database flavour
print "How many RAMs you need?"
flavors = CDB.list_flavors()
for pos, flavor in enumerate(flavors):
  print "%s: %s, %s" % (pos, flavor.name, flavor.ram)
#done

opt = raw_input("Pick a number - [almost] any number: ")
try:
  opt = int(opt)
  cdbram = flavors[opt]
except:
  print "I don't know how to '" + opt + "'.  Bail!"
  exit(1)


#
# Prompt for datadir size
print
opt = raw_input("How many jiggabytes you need for this bad mutha? ")
try:
  cdbdisk = int(opt)
except:
  print "640K is more memory than anyone will ever need.  Bail!"
  exit(1)


#
# Create the CDB instance
print
print "You and the captain, make it happen."
mycdb = CDB.create(cdbname, flavor=cdbram, volume=cdbdisk)
toggle = 0
while True:
  mycdb = CDB.get(mycdb.id)
  time.sleep(10)
  if mycdb.status != "BUILD":
    break
  #fi
  if toggle == 0:
    print "Workin' [in a coal mine, goin' down down down]..."
  else:
    print "Workin' [in a coal mine, whoop - about to slip down]..."
  #fi
  toggle=(toggle + 1) % 2
#done
print
print "Work's finished.  Here's what we have to show for it:"
print "Name:  ", mycdb.name
print "ID:    ", mycdb.id
print "Status:", mycdb.status
print "RAM:   ", mycdb.flavor.name
print "Disk:  ", mycdb.volume.size
print "URL:   ", mycdb.links[1]['href']

if mycdb.status != "ACTIVE":
  print
  print "Aw crap, time to issue credits."
  exit(1)
#fi


#
# Add some databases to the instance
print
print "It has been stated:"
print "The script should also create X number of Databases and X number"
print "of users in the new Cloud Database Instance."
opt = raw_input("How many is X? ")

try:
  numdbs = int(opt)
except:
  print "You have initiated the self-destruct sequence."
  print "Please enter a 65-digit prime number to abort: "
  time.sleep(2)
  # 97513779050322159297664671238670850085661086043266591739338007321
  exit(1)

print
for x in range(0, numdbs):
  mycdb.create_database("db" + str(x))
  print "Database 'db%s' has been created." % (x)
  mycdb.create_user("user"+str(x), "starwars", database_names="db"+str(x))
  print "User '%s' has been created on instance '%s'." % ("user"+str(x), mycdb.name)
#done
print
print "Even though the challenge said to 'Return the Cloud DB URL', it's not"
print "possible to use 'return' outside of a function.  All I've got to work"
print "with is exit status, so you'll have to settle for the URL printed out"
print "in the CDB instance summary above."
print


