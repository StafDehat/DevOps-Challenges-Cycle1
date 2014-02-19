#!/usr/bin/php

<?php
function is_valid_domain_name($domain_name) {
  return (preg_match("/^([a-z\d](-*[a-z\d])*)(\.([a-z\d](-*[a-z\d])*))*$/i", $domain_name) //valid chars check
       && preg_match("/^.{1,253}$/", $domain_name) //overall length check
       && preg_match("/^[^\.]{1,63}(\.[^\.]{1,63})*$/", $domain_name)   ); //length of each label
}
function is_valid_ip($address) {
  return (preg_match("/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/", $address));
}



$min = 1;
$max = 3;
$numservs = trim(fgets(STDIN));

while (filter_var($numservs, FILTER_VALIDATE_INT, array("options" => array("min_range"=>$min, "max_range"=>$max))) === FALSE) {
  echo "Error: Please enter 1, 2, or 3. \n";
  $numservs = trim(fgets(STDIN));
}

echo $numservs;

?>
