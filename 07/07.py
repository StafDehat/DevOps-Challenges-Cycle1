#!/usr/bin/env python

# Challenge 7: 
# Write a script that creates 2 Cloud Servers and a Cloud Load Balancer. Add 
# the 2 servers Private IP Addresses to the Load Balancer for port 80. For a 
# bonus point, add an Error page served via the Load Balancer for when none of 
# your nodes are available. Choose your language and SDK!

import os
import pyrax
import pprint
import inspect
import time
from auth import *


CS = pyrax.cloudservers
CLB = pyrax.cloud_loadbalancers
namebase = "andr4596"
numnodes = 2

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

#
# Create a list of nodes to be used for load balancing
nodes = []
for server in servers:
  node = CLB.Node(address=server.networks["private"][0], port=80, condition="ENABLED")
  nodes.append(node)
#done

#
# Build the load balancer
vip = CLB.VirtualIP(type="PUBLIC")
lb = CLB.create(namebase, port=80, protocol="HTTP", nodes=nodes, virtual_ips=[vip])

#
# Wait for load balancer to build
while True:
  lb = CLB.get(lb.id)
  time.sleep(10)
  print "Waiting on LB build..."
  if lb.status != "BUILD":
    break
  #fi
#done
print "LB no longer building."

#
# Confirm successful build
lb = CLB.get(lb.id)
if lb.status != "ACTIVE":
  print "ERROR: LB did not build successfully."
  exit(2)
#fi
print "LB built successfully"

#
# Add an error page & walk away
print "Adding error page to LB"
html = "<html><head><title>Whoops</title></head><body>All nodes are down.</body></html>"
lb.set_error_page(html)


print "All tasks complete"
