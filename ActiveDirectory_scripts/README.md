# Active Directory Scripts

---

## Security Identifier Converter (SID_converter.py)
Simple tool to convert Security Identifier (SID) -used in Active Directory- from readable/normal string to hexadecimal format and viceversa.


### str2hex
Convert SID to hexadecimal format. Example usage:

```shell-session
$ python3 SID_converter.py str2hex S-1-5-21-4088429403-1159899800-2753317549

[*] Given SID: S-1-5-21-4088429403-1159899800-2753317549
[*]   Hex SID: 0x0104000000000005150000005b7bb0f398aa2245ad4a1ca4
```

### hex2str
Convert SID in hexadecimal format to readable format/string. Example usage:
```shell-session
$ python3 SID_converter.py hex2str 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4

[*] Hex SID: 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4
[*] New SID: S-1-5-21-4088429403-1159899800-2753317549
```
