# Create Dictionary From File

A simple script to create a custom wordlist/dictionary based on a file if you suspect that one of the words in the file might be a potential password. Similar to [CeWL](https://github.com/digininja/CeWL), but only for a simple file.

## Usage
General usage:
```shell-session
python3 create_dictionary.py <input-file> <output-dictionary-file>
```
For example:

```shell-session
python3 create_dictionary.py randomfile.txt passwords.txt
```
