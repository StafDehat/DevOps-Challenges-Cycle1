#!/usr/bin/env python

# Challenge 8: 
# Write a script that creates a Cloud Performance 1GB Server. The script should
# then add a DNS "A" record for that server. Create a Cloud Monitoring Check and
# Alarm for a ping of the public IP address on your new server. Return to the 
# STDOUT the IP Address, FQDN, and Monitoring Entity ID of your new server. 
# Choose your language and SDK! 

import os
import sys
import pyrax
import pprint
import inspect
import time
from auth import *

CS = pyrax.cloudservers
DNS = pyrax.cloud_dns
CM = pyrax.cloud_monitoring
namebase = "andr4596"
parentZone=namebase + ".info"
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
  if flavor.id == "performance1-1":
    cssize = flavor
    break
  #fi
#done

#
# Initialize the builds
servers = []
for x in range(1,numnodes+1):
  servername = namebase + "-0" + str(x)
  servers.append(CS.servers.create(servername, csimage.id, cssize.id))
#done

#
# Wait for server builds to finish
for server in servers:
  while True:
    server = CS.servers.get(server.id)
    time.sleep(10)
    print "Waiting on " + server.name + "..."
    if server.status != "BUILD":
      break
    #fi
  #done
#done

#
# Confirm successful builds
for server in servers:
  server = CS.servers.get(server.id)
  if server.status != "ACTIVE":
    print "ERROR: Server '" + server.name + "' did not build successfully."
    exit(1)
  #fi
#done
print "Build finished successfully\n"

#
# add a DNS "A" record for that server
# To what zone?
print "Not sure what DNS zone to use..."
print "We're just gonna use " + parentZone + " as the parent zone."

#
# Search for a zone with this name
domid=-1
domains = DNS.list() #limit=100
while True:
  try:
    for domain in domains:
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
  print "Zone file does not exist."
  try:
    dom = DNS.create(name=parentZone, emailAddress="devnull@rootmypc.net",
                     ttl=900, comment="Challenge 08")
    domid=dom.id
    print "Zone file created."
  except exc.DomainCreationFailed as e:
    print("Zone file creation failed:", e)
    exit(1)
else:
  print "Zone file already exists."
#fi

#
# Create an A record
domain = DNS.get(domid)
a_rec = {"type": "A",
        "name": str(server.name) + "." + parentZone,
        "data": str(server.accessIPv4),
        "ttl": 86400}
domain.add_records([a_rec])
print "A record created.\n"

#
# Find entity of this cloud server
print "Checking for existing Cloud Monitoring entity for server."
CMents = CM.list_entities()
if CMents:
  for CMent in CMents:
    if CMent.label == server.name:
      print "Using Cloud Monitoring entity ID: " + CMent.id + "\n"
      break
    #fi
  #done
#fi

if not CMent.label == server.name:
  print "Couldn't find a Cloud Monitoring entity.  Making one."
  CMent = CM.create_entity(name=server.name, ip_addresses={"main": server.accessIPv4},
            metadata={"note": "Entity for server '%s'" % server.name})
  print "Name: " + CMent.name
  print "ID:   " + CMent.id
  print "IPs:  " + CMent.ip_addresses
  print "Meta: " + CMent.metadata + "\n"
#fi

#
# Create Cloud Monitoring check
zones = CM.list_monitoring_zones()
aliases = CMent.ip_addresses.items()
alias=aliases[0][0]
CMchk = CM.create_check(CMent, label="ping", check_type="remote.ping",
          details={"count": 5}, monitoring_zones_poll=zones,
          period=60, timeout=20, target_alias=alias)
print "Creating new ping check"
print "Name: " + CMchk.name
print "ID:   " + CMchk.id + "\n"

#
# Create Cloud Monitoring alarm
plans = CM.list_notification_plans()
CMalarm = CM.create_alarm(CMent, CMchk, plans[0],
      ("if (metric['available'] < 50) { return new AlarmStatus(CRITICAL, 'Packet loss is greater than 50%'); }"
       "return new AlarmStatus(OK, 'Packet loss is normal');"), label="ping")
print "Creating alarm/notification for that ping check"
print "Alarm ID: " + CMalarm.id + "\n"

#
# Print IP Address, FQDN, and Monitoring Entity ID
print "Consider this my return value:"
print "Server IP:  " + str(server.accessIPv4)
print "FQDN:       " + str(server.name) + "." + parentZone
print "Monitor ID: " + str(CMchk.id)



