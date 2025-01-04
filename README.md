# Deprecated
This code is deprecated and repo archived due to closure of ANX services.

ANX API Client
==============
This is an unofficial pythonic implementation of
[ANX's API](https://dyn.anx.se), described here [API documentation](http://dyn.anx.se/users/apidok.jsf)

Important information
---------------------
PLEASE DON'T USE EARLIER VERSIONS THEN 0.2.5 SINCE IT INCLUDED A BAD DEPENDENCY.

[request](https://mp-weixin-qq-com.translate.goog/s/dkPdXfGfSK097GI6Ln92lA?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp) was used instead of requests. This was not used in the code but as a install_requires in setup.py. 

PLEASE REMOVE EARLIER VERSIONS THAN 0.2.5.

This was included by mistake, unintentionally. 

Documentation
-------------
This is alpha state software, and I haven't bothered with documentation yet.

Command line client
-------------------
```
usage: main.py [-h] [-k APIKEY] [-d DOMAIN] [-v]
               {get,g,add,a,update,u,delete,d,del} ...

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
                        API key used in request header
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -v, --verbose         Verbose

Actions:
  {get,g,add,a,update,u,delete,d,del}
                        Action to perform
    get (g)             Get records
    add (a)             Add record
    update (u)          Update record
    delete (d, del)     Delete record
```

Client requires two parameters APIKEY and DOMAIN. These can be provided as ENV or arguments in the call.
```
export ANXDNS_APIKEY=keygoeshere
export ANXDNS_DOMAIN=domain.se
```
or
```
./bin/anxdnsclient -d domain.se --apikey keygoeshere
```

#### Examples
Get all records 
```
./bin/anxdnsclient -d domain.se --apikey keygoeshere get
```
Get records by name
```
./bin/anxdnsapi get -n www.domain.se -d domain.se --apikey keygoeshere
```

Get TXT records by txt
```
./bin/anxdnsapi get -t txtrecord -d domain.se --apikey keygoeshere
```

TODO
-----
* Update of names
* Test cases

Changelog
---------
##### Version 0.2.5
Released 10nd June 2022
Corrected typo in setup.py for the requests package.

##### Version 0.2
Released 10nd August 2019

- Initial release
