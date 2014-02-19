<?php

require_once('opencloud/lib/rackspace.php');

define('INIFILE', $_SERVER['HOME']."/.rackspace_php-opencloud_creds");
$ini = parse_ini_file(INIFILE, TRUE);
if (!$ini) {
    printf("Unable to load .ini file [%s]\n", INIFILE);
    exit;
}
$RAX = new OpenCloud\Rackspace(
    $ini['Identity']['url'], $ini['Identity']);

$RAX->SetDefaults('Compute',
    $ini['Compute']['serviceName'],
    $ini['Compute']['region'],
    $ini['Compute']['urltype']
);

$RAX->SetDefaults('ObjectStore',
    $ini['ObjectStore']['serviceName'],
    $ini['ObjectStore']['region'],
    $ini['ObjectStore']['urltype']
);

$RAX->SetDefaults('DbService',
    $ini['DbService']['serviceName'],
    $ini['DbService']['region'],
    $ini['DbService']['urltype']
);

?>

