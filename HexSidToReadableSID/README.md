# Hex SID to Readable SID

Suppose that we get an `SID` of a domain using a service such as `M̀SSQL`. We can request the `Domain SID` with:

```sql
DECLARE @sid VARBINARY(85) = SUSER_SID('DOMAIN\Administrator'); DECLARE @len INT = DATALENGTH(@sid) - 4; SELECT 'Domain SID' AS label, CONVERT(VARCHAR(1000), SUBSTRING(@sid, 1, @len), 1) AS domain_sid_hex;
```
Where `DOMAIN` is the domain name. This will return a domain in hex.

Then, we can use this hex string and pass it to a readable format with the script:
```shell-session
python3 hex_to_sid.py 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4
```
