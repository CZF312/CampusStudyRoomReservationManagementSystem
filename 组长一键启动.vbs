' Legacy launcher — prompts MySQL password then runs unified start.bat
Option Explicit
Dim sh, fso, root, batPath, pwd
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = root & "\start.bat"

If Not fso.FileExists(batPath) Then
    MsgBox "未找到 start.bat，请确认从 Git 完整下载项目。", vbCritical, "CSRRMS"
    WScript.Quit 1
End If

If Not fso.FileExists(root & "\pom.xml") Then
    MsgBox "请在含 pom.xml 的项目根目录运行本启动器。", vbCritical, "CSRRMS"
    WScript.Quit 1
End If

pwd = InputBox("请输入本机 MySQL 的 root 密码：" & vbCrLf & vbCrLf & _
    "（仅保存在本机，不会上传到 GitHub）", "校园自习室系统 - 一键启动", "")
If pwd = "" Then
    MsgBox "已取消。", vbInformation, "CSRRMS"
    WScript.Quit 0
End If

sh.Environment("Process")("CSRRM_MYSQL_PASSWORD") = pwd
sh.CurrentDirectory = root
sh.Run "cmd /c """ & batPath & """", 1, True
