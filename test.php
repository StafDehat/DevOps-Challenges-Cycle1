<?php
//__Challenge 3__: Write a script that prints a list of all of the DNS domains on an account. Let the user select a domain from the list and add an "A" record to that domain by entering an IP Address TTL, and requested "A" record text. This must be done in PHP with php-opencloud.

// First we need to include our auth script and some needed tools
require_once('./auth.php');

// Now we set some common variables
$DNS = $RAX->DNS();
$DNSList = $DNS->DomainList();
$test = FALSE;

// First we are going to list the current Domains
echo ("Here is a list of your current Domain names \n \n");

while ($Zone = $DNSList->Next()) {
echo ("$Zone->name \n");
}

// Now that we know what domains exist we can let the user pick one
echo ("Which of the above domains would you like to create an A record for? \n");

$domain = trim(fgets(STDIN));

// As always we need to make sure a cat did not walk accross the keyboard

while (!$test) {
while ($Zone = $DNSList->Next()) {
echo ("this is a test \n");
if ($Zone->name === $domain) {
$test = TRUE;
break;
}
else {
var_dump($Zone->name);
}
}	

var_dump($test);

if (!$test) {
echo "Please enter one of the domains above. \n";
$domain = trim(fgets(STDIN));
}
}

echo ($test);
echo ($domain);


?>
