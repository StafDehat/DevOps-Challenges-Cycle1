<?php

// __Challenge 2__:
// Write a script that builds anywhere from 1 to 3 512MB cloud servers (the number is based on user input). Inject an SSH public key into the server for login. Return the IP addresses for the server. The servers should take their name from user input, and add a numerical identifier to the name. For example, if the user inputs "bob", the servers should be named bob1, bob2, etc... This must be done in PHP with php-opencloud. 

require_once('opencloud/lib/rackspace.php');
require_once('./auth.php');

// Some hard-coded crap
$cent63id = 'c195ef3b-9195-4474-b6f7-16e5bd86acd0';

$compute = $RAX->Compute();

function usage($self) {
  echo "Usage: php $self num-servers hostname-base [SSH-public-key-file]\n";
  echo "  num-servers:         Must be 1, 2, or 3.\n";
  echo "  hostname-base:       Must be alpha-numeric.\n";
  echo "  SSH-public-key-file: Optional.  Must be path to a readable file.\n";
  echo "                       If no file is passed, will search for pubkey at\n";
  echo "                       ~/.ssh/id_dsa.pub and ~/.ssh/id_rsa.pub\n";
  exit;
}

if (count($argv) > 4 || count($argv) < 3) {
  echo "Error: Incorrent number of arguments.\n";
  usage($argv[0]);
}

// Sanitize numServers input
$numServers = $argv[1];
if (! ctype_digit($numServers) ) {
  echo "Error: num-servers must be numeric.\n";
  usage($argv[0]);
} else if ($numServers < 1 || $numServers > 3) {
  echo "Error: num-servers must be 1, 2, or 3.\n";
  usage($argv[0]);
} else {
  echo "Creating $numServers server(s).\n";
}

// Sanitize hostnameBase input
$hostnameBase = $argv[2];
if (! ctype_alnum($hostnameBase)) {
  echo "Error: hostname-base must be alpha-numeric.\n";
  usage($argv[0]);
} else {
  echo "Using \"$hostnameBase\" as server hostname prefix.\n";
}


// Grab SSH public keys from workstation:
$authkeys = "";
$homedir = $_SERVER['HOME'];

// If SSH pubkey was passed as argument, upload it
if (count($argv) == 4 ) {
  $localkey = $argv[3];
  // Verify provided directory exists
  if ( file_exists($localkey) &&
       is_readable($localkey) ) {
    echo "Found public SSH key at \"$localkey\" - Gonna upload it.\n";
    $authkeys = $authkeys ."\n". file_get_contents($localkey);
  }
} else if ( file_exists( "$homedir/.ssh/id_rsa.pub" ) &&
     is_readable( "$homedir/.ssh/id_rsa.pub" ) ) {
  echo "Found public SSH key at \"$homedir/.ssh/id_rsa.pub\" - Gonna upload it.\n";
  $authkeys = $authkeys ."\n". file_get_contents("$homedir/.ssh/id_rsa.pub");
} else if ( file_exists( "$homedir/.ssh/id_dsa.pub" ) &&
     is_readable( "$homedir/.ssh/id_dsa.pub" )) {
  echo "Found public SSH key at \"$homedir/.ssh/id_dsa.pub\" - Gonna upload it.\n";
  $authkeys = $authkeys ."\n". file_get_contents("$homedir/.ssh/id_dsa.pub");
} else {
  echo "Error: No SSH key provided, and can not find one in ~/.ssh/\n";
  usage($argv[0]);
}


$servers = array();

// Initiate the creation of all servers - store their initial details in an array
for ($x=1; $x<=$numServers; $x++) {
  $server = $compute->Server();
  $server->name = $hostnameBase . $x;
  $server->flavor = $compute->Flavor(2); //512MB
  $server->image = $compute->Image($cent63id);
  $server->AddFile("/root/.ssh/authorized_keys", $authkeys);
  $server->Create();

  $servers[] = $server;

  echo "Creating server " . $server->name . " with ID ". $server->id ."\n";
}


// Wait for build completion, pull updated details and print info
for ($x=0; $x<count($servers); $x++) {
  $server = $servers[$x];
  $id = $server->id;
  $rootpass = $server->adminPass;

  // Wait for servers to finsih building
  do {
    echo "Server not yet active.  Sleeping 30s...\n";
    sleep(30);
    $server = $compute->Server($id);
  } while ( $server->status == 'BUILD' );

  // Verify build completed successfully
  if (!($server->status == 'ACTIVE')) {
    echo "Unknown error encountered while building server $server->name\n";
    echo "Server status: $server->status\n";
    exit;
  }

  // Report server details
  echo "\n";
  echo $server->name . " details:\n";
  echo "Server ID: ". $id ."\n";
  echo "IP:        " . $server->ip(4) . "\n";
  echo "Username:  root\n";
  echo "Password:  " . $rootpass . "\n";
  echo "\n";
}

?>
