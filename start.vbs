' Double-click launcher — if this file does not respond, use start.bat
Option Explicit
Dim sh, root, batPath
Set sh = CreateObject("WScript.Shell")
root = Replace(WScript.ScriptFullName, WScript.ScriptName, "")
batPath = root & "start.bat"
If Not CreateObject("Scripting.FileSystemObject").FileExists(batPath) Then
    MsgBox "start.bat not found in project root.", vbCritical, "CSRRMS"
    WScript.Quit 1
End If
sh.CurrentDirectory = root
sh.Run "cmd /c """ & batPath & """", 1, True
