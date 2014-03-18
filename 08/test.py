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

cs = pyrax.cloudservers
DNS = pyrax.cloud_dns
CM = pyrax.cloud_monitoring


server_name = pyrax.utils.random_ascii(8)

ubu_image = [img for img in cs.images.list()
  if "12.04" in img.name][0]
print("Ubuntu Image:", ubu_image)

for flavor in cs.flavors.list():
  if flavor.id == "performance1-1":
    print "FOUND IT"
#done

