# Webmin 1.920 Remote Code Execution (Unauthenticated) - CVE-2019-15107

Exploit based on [CVE-2019-15107](https://nvd.nist.gov/vuln/detail/CVE-2019-15107).

## Usage
```shell-session
python3 CVE-2019-15107.py -u <victim-IP-adress> -c <command-to-execute>
```

For example:
```shell-session
python3 CVE-2019-15107.py -u 'http://10.10.10.245:10000' -c 'cat /etc/passwd'
```
