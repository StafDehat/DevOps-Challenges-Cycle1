<?php

// __Challenge 4__:
// Write a script that creates a Cloud Files Container. If the container already exists, exit and let the user know. The script should also upload a directory from the local filesystem to the new container, and enable CDN for the new container. The script must return the CDN URL. This must be done in PHP with php-opencloud. 


require_once('opencloud/lib/rackspace.php');
require_once('./auth.php');

$ostore = $RAX->ObjectStore();

function usage($self) {
  echo "Usage: php $self cloud-files-container local-directory\n";
  exit;
}


// Ensure proper number of args
if (count($argv) != 3) {
  echo "Error: Incorrent number of arguments.\n";
  usage($argv[0]);
}

$containerName = $argv[1];
$localDir = $argv[2];


// Ensure container name is valid
if (! ctype_alnum($containerName)) {
  echo "Error: Container name's gotta be alpha-numeric, bro.\n";
  usage($argv[0]);
}


// Test if container exists in cloud files
$exists = false;
$containerList = $ostore->ContainerList();
while($container = $containerList->Next()) {
  if ($container->name == $containerName) {
    echo "Error: Container \"$containerName\" already exists.\n";
    usage($argv[0]);
  }
}


// Validate that local directory exists & is readable
if (! is_dir($localDir)) {
  echo "Error: Specified directory does not exist.\n";
  usage($argv[0]);
}
if (! is_readable($localDir) ) {
  echo "Error: Unable to open directory \"$localDir\".\n";
  usage($argv[0]);
}


// Create container
echo "Creating container \"$containerName\"\n";
$container = $ostore->Container();
$container->name = $containerName;
$container->Create();

// Verify container got created.
$containerList = $ostore->ContainerList(array("name"=>$containerName));
if (count($containerList) < 1) {
  echo "Unknown error occurred while creating container.\n";
  exit;
}
echo "Container created successfully.\n";

// Enable CDN
echo "Enabling CDN on container.\n";
$container->EnableCDN();


// Upload directory to container
if ($handle = opendir($localDir)) {
  while (false !== ($file = readdir($handle))) {
    if (is_file($localDir."/".$file)) {
      if (is_readable($localDir."/".$file)) {
        // Upload file to new Cloud Files container
        $CFfile = $container->DataObject();
        $CFfile->Create(array('name'=>$file), "$localDir/$file");
      } else {
        echo "Skipping file \"$localDir/$file\" - unable to read.\n";
      }
    } else {
      echo "Skipping directory \"$localDir/$file\".\n";
    }
  }
  closedir($handle);
} else {
  echo "Error: Unable to open directory \"$localDir\".\n";
  usage($argv[0]);
}


// Output CDN URL
echo "Container CDN URL: ". $container->PublicURL() ."\n";


?>
