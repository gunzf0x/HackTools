# Port Scanner
An option if, for some reason, the system does not have commands such as `ss` or `netstat` to analyze internal TCP ports open; or `nmap` or `masscan` for external ports open.

## portscanner.py

[Python](https://www.python.org/) script option:

```shell-session
$ python3 portscanner.py <IP> <START-PORT> <END-PORT>
```

For example:
```shell-session
$ python3 portscanner.py 192.168.1.10 1 65535
```

## portscanner.sh
[Bash](https://ryanstutorials.net/bash-scripting-tutorial/bash-script.php) script option:
```shell-session
$ ./portscanner.sh <IP> <START-PORT> <END-PORT> <THREADS>
```

For example:
```shell-session
$ ./portscanner.sh 192.168.1.10 1 65535 30
```
or
```shell-session
$ bash portscanner.sh 192.168.1.10 1 65535 30 
```
