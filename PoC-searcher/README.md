# PoC Searcher on Github

It uses [https://poc-in-github.motikan2010.net/](https://poc-in-github.motikan2010.net/) API to search for PoCs available at Github.

A great alternative to directly search for PoCs at Github rather than losing our time Googling.

## Usage

```shell-session
$ python3 PoC_searcher.py -- help

usage: PoC_searcher.py [-h] {latest,search,parameter} ...

Proof of Concepts searcher from Github

options:
  -h, --help            show this help message and exit

commands:
  {latest,search,parameter}
    latest              Get the latest #N PoCs registered/uploaded at Github
    search              Search for CVEs PoCs uploaded to Github
    parameter           Search PoCs by parameters such as popularity, dates, etc
```

### 'latest' command
Search for the N latest PoCs detected at Github. For example, search for the latest 1000 PoCs registered and also search if the word `gunzf0x` is present in any of the fields to filter data:

```shell-session
$ python3 PoC_searcher.py latest --limit 1000 -f gunzf0x

======================================================== CVE Github Searcher | LATEST ========================================================
[+] Github CVE Searcher | 'latest': Data extracted from API
[+]  Retreiving data for the latest 1000 PoCs uploaded to Github...

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[+] ID: 787180944
[+] CVE ID: CVE-2024-0986
[+] Name: Issabel-PBX-4.0.0-RCE-Authenticated
[+] Owner: gunzf0x
[+] HTML URL: https://github.com/gunzf0x/Issabel-PBX-4.0.0-RCE-Authenticated
[+] Description: Issabel PBX 4.0.0 Remote Code Execution (Authenticated) - CVE-2024-0986
[+] Stargazers Count: 0
[+] Vulnerability Description: A vulnerability was found in Issabel PBX 4.0.0. It has been rated as critical. This issue affects some unknown processing of the file /index.php?menu=asterisk_cli of the component Asterisk-Cli. The manipulation of the argument Command leads to os command injection. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. The associated identifier of this vulnerability is VDB-252251. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.
[+] Created At: 2024-04-16 12:24:25
[+] Updated At: 2024-04-16 12:33:42
[+] Pushed At: 2024-04-16 12:55:14
[+] Inserted At: 2024-04-16 16:39:08
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------```
```


### 'search' command
Search for by CVE ID. For example:

```shell-session
$ python3 PoC_searcher.py search --name 'cve 2024 1086'

======================================================== CVE Github Searcher | SEARCH ========================================================
[+] Github CVE Searcher | 'search': Data extracted from API

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[+] ID: 775151369
[+] CVE ID: CVE-2024-1086
[+] Name: CVE-2024-1086
[+] Owner: Notselwyn
[+] HTML URL: https://github.com/Notselwyn/CVE-2024-1086
[+] Description: Proof-of-concept exploit for CVE-2024-1086, working on most Linux kernels between (including) v5.14 and (including) v6.6, including (but not limited to) Debian, Ubuntu, and KernelCTF.
[+] Stargazers Count: 0
[+] Vulnerability Description: A use-after-free vulnerability in the Linux kernel's netfilter: nf_tables component can be exploited to achieve local privilege escalation.

The nft_verdict_init() function allows positive values as drop error within the hook verdict, and hence the nf_hook_slow() function can cause a double free vulnerability when NF_DROP is issued with a drop error which resembles NF_ACCEPT.

We recommend upgrading past commit f342de4e2f33e0e39165d8639387aa6c19dff660.


[+] Created At: 2024-03-21 06:16:41
[+] Updated At: 2024-03-21 06:17:44
[+] Pushed At: 2024-03-21 06:17:37
[+] Inserted At: 2024-03-21 10:38:47
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```


### 'parameter' command
Filter results by a parameter such as `stargazer` or `popular`, `created` or `updated`. For example:

```shell-session
$ python3 PoC_searcher.py parameter popular

[↗] Github CVE Searcher | 'parameter': Making request to 'https://poc-in-github.motikan2010.net/api/v1/?sort=stargazers_count&limit=2'...

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[+] ID: 437729997
[+] CVE ID: CVE-2021-44228
[+] Name: log4j-scan
[+] Owner: fullhunt
[+] HTML URL: https://github.com/fullhunt/log4j-scan
[+] Description: A fully automated, accurate, and extensive scanner for finding log4j RCE CVE-2021-44228
[+] Stargazers Count: 2884
[+] Vulnerability Description: Apache Log4j2 2.0-beta9 through 2.15.0 (excluding security releases 2.12.2, 2.12.3, and 2.3.1) JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From version 2.16.0 (along with 2.12.2, 2.12.3, and 2.3.1), this functionality has been completely removed. Note that this vulnerability is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging Services projects.
[+] Created At: 2021-12-13 12:57:50
[+] Updated At: 2022-05-22 01:26:13
[+] Pushed At: 2022-05-17 22:25:17
[+] Inserted At: None
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[+] ID: 252131233
[+] CVE ID: CVE-2019-17558
[+] Name: exphub
[+] Owner: zhzyker
[+] HTML URL: https://github.com/zhzyker/exphub
[+] Description: Exphub[漏洞利用脚本库] 包括Webloigc、Struts2、Tomcat、Nexus、Solr、Jboss、Drupal的漏洞利用脚本，最新添加CVE-2020-14882、CVE-2020-11444、CVE-2020-10204、CVE-2020-10199、CVE-2020-1938、CVE-2020-2551、CVE-2020-2555、CVE-2020-2883、CVE-2019-17558、CVE-2019-6340
[+] Stargazers Count: 3321
[+] Vulnerability Description: Apache Solr 5.0.0 to Apache Solr 8.3.1 are vulnerable to a Remote Code Execution through the VelocityResponseWriter. A Velocity template can be provided through Velocity templates in a configset `velocity/` directory or as a parameter. A user defined configset could contain renderable, potentially malicious, templates. Parameter provided templates are disabled by default, but can be enabled by setting `params.resource.loader.enabled` by defining a response writer with that setting set to `true`. Defining a response writer requires configuration API access. Solr 8.4 removed the params resource loader entirely, and only enables the configset-provided template rendering when the configset is `trusted` (has been uploaded by an authenticated user).
[+] Created At: 2020-04-01 18:33:35
[+] Updated At: 2022-05-21 16:02:40
[+] Pushed At: 2021-04-04 18:13:57
[+] Inserted At: None
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
