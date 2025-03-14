# HacktheBox Avatar Extractor

A tool to extract avatars from HackTheBox oficial page. This tool automatically extract avatars from [HackTheBox official machines page](https://www.hackthebox.com/machines/).

## Usage
To extract avatar from with name `<machine-name>`, pass it to `-n`/`--name` flag and execute:
```shell-session
python3 HTB_Avatar_Extractor.py -n <machine-name>
```

For example, to extract content for [Mist](https://www.hackthebox.com/machines/mist) machine, execute:
```shell-session
python3 HTB_Avatar_Extractor.py -n mist
```

It will copy the avatar url link to clipboard.

### Obsidian output
Since I have designed this tool to use it for my [Obsidian](https://obsidian.md/) notes, just use `-o` or `--obsidian` flag to copy the url link to display it on `Obsidian`.

For example, running:
```shell-session
python3 HTB_Avatar_Extractor.py -n mist -o
```
Will copy to our clipboard:
```
![Avatar mist](https://labs.hackthebox.com/storage/avatars/84669b838a8633d26f4a2d90a6069f7e.png)
```
Pasting this content into `Obsidian` will automatically display the image.
