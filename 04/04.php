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


// Lots of helpers to upload recursively
function fileUnder5G($handle) {
  return filesize($handle) < 1024 * 1024 * 1024 * 5;
}

function uploadSmallFile($topDir, $subDir, $filename) {
  $container = $GLOBALS['container'];
  $dirPrefix = str_replace("/", "_", $subDir);
  $CFName = $dirPrefix ."_". $filename;
  echo "Uploading '$topDir/$subDir/$filename' as '$CFName'\n";
  $CFfile = $container->DataObject();
  $CFfile->Create(array('name'=>$CFName), "$topDir/$subDir/$filename");
}

function uploadLargeFile($topDir, $subDir, $filename) {
  $container = $GLOBALS['container'];
  $dirPrefix=str_replace("/", "_", $subDir);
  $CFName = $dirPrefix ."_". $filename;
  echo "Uploading '$topDir/$subDir/$filename' as '$CFName'\n";
  $transfer = $container->setupObjectTransfer(array(
    'name' => $CFName,
    'path' => "$topDir/$subDir/$filename",
    'concurrency' => 4,
    'partSize'    => 1.0 * Size::GB
  ));
  $transfer->upload();
}

function uploadFile($topDir, $subDir, $filename) {
  if (fileUnder5G("$topDir/$subDir/$filename")) {
    uploadSmallFile($topDir, $subDir, $filename);
  } else {
    uploadLargeFile($topDir, $subDir, $filename);
  }
}

function uploadDir($topDir, $subDir) {
  //echo "Entering directory: $topDir/$subDir\n";
  if (! $handle = opendir("$topDir/$subDir")) {
    echo "Error: Unable to open directory \"$topDir/$subDir\".\n";
    exit(1);
  }
  $contents = scandir("$topDir/$subDir");
  foreach ($contents as $handle) {
    if (is_link("$topDir/$subDir/$handle")) {
      echo "Skipping symlink: $topDir/$subDir/$handle\n";
    } elseif (is_dir("$topDir/$subDir/$handle")) {
      if ( $handle === "." || $handle === ".." ) {
        //echo "Ignoring directory: $topDir/$subDir/$handle\n";
      } else {
        uploadDir($topDir, "$subDir/$handle");
      }
    } elseif (is_file("$topDir/$subDir/$handle")) {
      uploadFile($topDir, $subDir, $handle);
    } else {
      echo "Ignoring unknown 'file': $topDir/$subDir/$handle \n";
    }#fi
  }#done
}

// Upload directory recursively
uploadDir($localDir, "");

// Output CDN URL
echo "\nContainer CDN URL: ". $container->PublicURL() ."\n";


?>
