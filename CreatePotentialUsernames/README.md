# CreatePotentialUsernames
A simple tool to create a potential list of usernames based on a list of names (firstnames and lastnames)

## Usage
Assume that we have a potential list of usernames in a file called `example_usernames.txt`, then pass it using `-l / --list` flag and try:
```shell-session
python3 create_potential_usernames.py -l example_usernames.txt
```
this will create a list with potential usernames called `potential_usernames.txt` in the current directory. 
You can specify your own outfile name with `-o / --outfile` flag.

You can also add `--add-numbers` flag so the list of user generated will have, additionally, a number appended at the end of it. So, `fsmith` also becomes `fsmith1`, `fsmith2` and so on for every combination created...
