<?php

// __Challenge 3__:
// Write a script that prints a list of all of the DNS domains on an account. Let the user select a domain from the list and add an "A" record to that domain by entering an IP Address TTL, and requested "A" record text. This must be done in PHP with php-opencloud. 

require_once('opencloud/lib/rackspace.php');
require_once('./auth.php');

$dns = $RAX->DNS();


function is_valid_domain_name($domain_name) {
  return (preg_match("/^([a-z\d](-*[a-z\d])*)(\.([a-z\d](-*[a-z\d])*))*$/i", $domain_name) //valid chars check
       && preg_match("/^.{1,253}$/", $domain_name) //overall length check
       && preg_match("/^[^\.]{1,63}(\.[^\.]{1,63})*$/", $domain_name)   ); //length of each label
}
function is_valid_ip($address) {
  return (preg_match("/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/", $address));
}


// Print all domains in DNS for this account
$domainlist = $dns->DomainList();
$exists = false;
echo "List of zones:\n";
while($zone = $domainlist->Next()) {
  echo $zone->name ."\n";
}


$stdin = fopen('php://stdin', 'r');

// Parent domain loop
while (true) {
  // Prompt for user input - a domain
  echo "Enter domain name under which new A record will be created:\n";
  $domain = trim(fgets(STDIN));
  // Validate input - numeric option or ctype_alnum+'.'
  if (! is_valid_domain_name($domain)) {
    echo "Error: Invalid domain name.\n\n";
  } else {
    // Verify domain entered exists
    $domainlist = $dns->DomainList();
    while($zone = $domainlist->Next()) {
      if ($zone->name == "$domain") {
        $exists = 1;
        break;
      }
    }
    if ($exists) { break; }
    else { echo "Error: Specified domain does not exist.\n\n"; }
  } // End if-else
} // End loop
// $domain is now guaranteed valid and exists
echo "\n";


// Subdomain loop
while (true) {
  echo "Enter subdomain, with or without domain suffix:\n";
  $subdomain = trim(fgets(STDIN));
  $subdomain = preg_replace("/\.$domain$/", "", $subdomain);
  if (! is_valid_domain_name($subdomain .".". $domain)) {
    echo "Error: Invalid subdomain.\n\n";
  } else {
    break;
  }
} // End loop
echo "\n";


// TTL loop
while (true) {
  echo "Enter TTL for new A record in seconds:\n";
  $TTL = trim(fgets(STDIN));
  if (! ctype_digit($TTL)) {
    echo "Error: Invalid TTL - gotta be numeric.\n\n";
  } else {
    break;
  }
} // End loop
echo "\n";


// IP address loop
while (true) {
  echo "Enter IP for new A record:\n";
  $IP = trim(fgets(STDIN));
  if (! is_valid_ip($IP)) {
    echo "Error: Invalid IP address.\n\n";
  } else {
    break;
  }
} // End loop
echo "\n";


// Create A record
$record = $zone->Record();
$record->name = "$subdomain.$domain";
$record->type = "A";
$record->ttl = $TTL;
$record->data = $IP;
$record->Create();
$zone->Update();
echo "Added A record for \"$subdomain\" to zone file for \"$domain\":\n";
echo "$subdomain.$domain. IN A $TTL $IP\n";

?>
