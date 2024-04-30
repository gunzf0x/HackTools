# Temportal HTTP POST server
The classic `python3 -m http.server` is useful to share files and check if another machine has a connection to our machine. However, there might be some times that we need a victim machine to send us a `POST` request.

It is an alternative to `netcat`.

## Usage
```shell-session
$ python3 temporal_HTTP_server_for_POST_req.py -p 8080 
```
so we will start "listening" on port `8080`

Also, sometimes the data we might receive could be urlencoded. If that is the case, sue the flag `--url-decode-output` to automatically decode the received output.
