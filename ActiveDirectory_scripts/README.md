# Active Directory Scripts

---

## Security Identifier Converter (SID_converter.py)
Simple tool to convert Security Identifier (SID) -used in Active Directory- from readable/normal string to hexadecimal format and viceversa.


### str2hex
Convert SID to hexadecimal format:

```shell-session
$ python3 SID_converter.py str2hex S-1-5-21-4088429403-1159899800-2753317549

[*] Given SID: S-1-5-21-4088429403-1159899800-2753317549
[*]   Hex SID: 0x0104000000000005150000005b7bb0f398aa2245ad4a1ca4
```

### hex2str
Convert SID in hexadecimal format to readable format/string:
```shell-session
$ python3 SID_converter.py hex2str 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4

[*] Hex SID: 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4
[*] New SID: S-1-5-21-4088429403-1159899800-2753317549
```

### str2-base64
Convert SID to base64 format (as shown in LDAP service):
```shell-session
$ python3 SID_converter.py str2-b64 S-1-5-21-2570265163-3918697770-3667495639-1235

[*]  Given SID: S-1-5-21-2570265163-3918697770-3667495639-1235
[*] Base64 SID: AQUAAAAAAAUVAAAASyIzmSqVkunXipna0wQAAA==
```

### b64-2str
Convert `objectSID` attribute from LDAP, that is in base64, to a valid SID format:
```shell-session
$ python3 SID_converter.py b64-2str AQUAAAAAAAUVAAAASyIzmSqVkunXipna0wQAAA==

[*] b64 SID: AQUAAAAAAAUVAAAASyIzmSqVkunXipna0wQAAA==
[*] New SID: S-1-5-21-2570265163-3918697770-3667495639-1235
```
