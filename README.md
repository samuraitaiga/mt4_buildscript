mt4 build script
=========

build script for mt4 project. put dodo.py into mt4 MQL folder then execute command "doit" then compiling and archiving are complete.

  - build mq4 files in Experts and Libraries folder
  - archive compiled files
  - compile is passed if mq4 file is not changed after compiling.
  - download compiler from internet

mt4 build script are written by doit(python).

Version
----

0.1

Requirements
--------------
 * python 2.7.3 or higher
 * pip 1.2.1 or higher

Installation
--------------
* install dependencies
```sh
pip install -r requirements.txt
```

How to use
--------------
1. put dodo.py into MQL folder. After mt4 build 600, MQL folder is [ C:\Users\USER NAME\AppData\Roaming\MetaQuotes\Terminal\HASH\MQL4 ]
1. execute command

```sh
# execute all task
doit

# execute specific task
doit build_mql

# list all task
doit list

# clean compiled files like make clean
doit clean
```


License
----

MIT

