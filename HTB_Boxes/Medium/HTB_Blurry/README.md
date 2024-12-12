# HTB Blurry

WriteUp: [https://gunzf0x.github.io/pentesting/posts/blurry/](https://gunzf0x.github.io/pentesting/posts/blurry/)

Script for [HTB Blurry](https://www.hackthebox.com/machines/blurry) machine that creates a malicious `pickle` file and executes it, leading to remote code execution.

## Usage

## Create malicious pickle file
Create a virtual enrvironment and install all the needed dependencies there
```shell-session
❯ python3 -m venv clearML_venv

❯ source clearML_venv/bin/activate

❯ pip3 install clearml
```
Then run the script:
```shell-session
❯ python3 malicious_pickle.py -c '<command>'
```

## Inject pytorch code
```shell-session
python3 create_malicious_pth.py
```
