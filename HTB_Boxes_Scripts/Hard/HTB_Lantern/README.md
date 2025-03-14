# HTB Lantern

WriteUp: [https://gunzf0x.github.io/pentesting/posts/lantern/](https://gunzf0x.github.io/pentesting/posts/lantern/)

Scripts for [HTB Lantern](https://www.hackthebox.com/machines/lantern) machine.

## Usage
First, create a `C#` project:
```shell-session
❯ dotnet new classlib -n revshell
```

Install needed packages:
```shell-session
❯ dotnet add package Microsoft.AspNetCore.Components --version 6.0.0 && dotnet add package Microsoft.AspNetCore.Components.Web --version 6.0.0
```

Enter in the project directory named `revshell` and edit `Class1.cs` file with the content of the file in the repo.

Finally, build the file:
```shell-session
❯ dotnet build -c release
```
