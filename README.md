SpamNinja
=========

This tool queries all ip networks of a company from Ripe and blocks them.


Installation
------------

Edit your `main.cf`:

```
smtpd_client_restrictions = check_client_access cidr:/etc/postfix/cidr_spamninja
```

Then setup spamninja.py as a cronjob


Thanks to
---------

- http://www.blackmanticore.com/040629229fdd3e219551e3e3fd8f2396
