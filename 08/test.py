#!/usr/bin/env python

# Challenge 8: 
# Write a script that creates a Cloud Performance 1GB Server. The script should
# then add a DNS "A" record for that server. Create a Cloud Monitoring Check and
# Alarm for a ping of the public IP address on your new server. Return to the 
# STDOUT the IP Address, FQDN, and Monitoring Entity ID of your new server. 
# Choose your language and SDK! 

import os
import pyrax
import pprint
import inspect
import time
from auth import *

CS = pyrax.cloudservers
DNS = pyrax.cloud_dns
namebase = "andr4596"
parentZone="andr4596.info"
numnodes = 1

# Set csimage
for img in CS.images.list():
  if "CentOS " in img.name:
    csimage = img
    break
  #fi
#done

# Set cssize
for flavor in CS.flavors.list():
  if flavor.ram == 1024:
    cssize = flavor
    break
  #fi
#done

#
# add a DNS "A" record for that server
# To what zone?
pubip = server.networks["public"][0]
print "We're just gonna use " + parentZone + " as the parent zone."

#
# Search for a zone with this name
domid=-1
domains = DNS.list() #limit=100
while True:
  try:
    for domain in domains:
      print("Domain:", domain.name)
      if domain.name == parentZone:
        domid=domain.id
        raise Exception("DomainFound");
      #fi
    #done
    domains = DNS.list_next_page()
  except:
    break
  #try
#done

#
# If we found it, domid is its ID.  If not, create it.
if domid == -1:
  print "Domain does not exist."
  try:
    dom = DNS.create(name=parentZone, emailAddress="devnull@rootmypc.net",
                     ttl=900, comment="Challenge 08")
    domid=dom.id
    print "Domain created in DNS."
  except exc.DomainCreationFailed as e:
    print("Domain creation failed:", e)
    exit(1)
else:
  print "Domain already exists in DNS."
#fi
print "ID: " + str(domid)

#
# Create a record
domain = DNS.get(domid)
a_rec = {"type": "A",
        "name": str(server.name) + "." + parentZone,
        "data": str(server.networks["public"][0]),
        "ttl": 86400}
domain.add_records([a_rec])

#
# Create a Cloud Monitoring Check and
# Alarm for a ping of the public IP address on your new server.


#
# Print IP Address, FQDN, and Monitoring Entity ID





