#!/usr/bin/env python

import os
import pyrax
import pyrax.exceptions as exc

pyrax.set_setting("identity_type", "rackspace")

# Use a credential file in the format:
# [rackspace_cloud]
# username = myusername
# api_key = 01234567890abcdef
print
print "Using credentials file"

# Note: you can name this file whatever you like.
creds_file = os.path.expanduser("~/.rackspace_pyrax_creds")
try:
    pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
    print "Did you remember to replace the credential file with your actual",
    print "username and api_key?"
print "authenticated =", pyrax.identity.authenticated
print

