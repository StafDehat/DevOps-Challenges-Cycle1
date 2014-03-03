#!/usr/bin/env python

# Challenge 7: 
# Write a script that creates 2 Cloud Servers and a Cloud Load Balancer. Add 
# the 2 servers Private IP Addresses to the Load Balancer for port 80. For a 
# bonus point, add an Error page served via the Load Balancer for when none of 
# your nodes are available. Choose your language and SDK!

import os
import pyrax
import pprint

CS = pyrax.cloudservers
CLB = pyrax.cloud_loadbalancers
namebase = "andr4596"
numnodes = 2

# Set csimage
for img in CS.images.list():
  if "CentOS 6.4" in img.name:
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
    if server.status != "ACTIVE":
      break
    #fi
  #done
#done

pprint.pprint(server)

#
# Build a load balancer with the cloud servers as nodes
nodes = []
for server in servers:
  node = clb.Node(address=server., port=80, condition="ENABLED")
  vip = clb.VirtualIP(type="PUBLIC")
  lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=[node], virtual_ips=[vip])
#done





