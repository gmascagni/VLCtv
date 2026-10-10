Set objArgs = Wscript.Arguments
If objArgs.Count = 0 Then Wscript.Quit

rawUrl = objArgs(0)

' Strip vlc:// or vlc:
If LCase(Left(rawUrl, 6)) = "vlc://" Then
    cleanUrl = Mid(rawUrl, 7)
ElseIf LCase(Left(rawUrl, 4)) = "vlc:" Then
    cleanUrl = Mid(rawUrl, 5)
Else
    cleanUrl = rawUrl
End If

' Remove trailing slash if present
If Right(cleanUrl, 1) = "/" Then
    cleanUrl = Left(cleanUrl, Len(cleanUrl) - 1)
End If

Set objFSO = CreateObject("Scripting.FileSystemObject")
vlcPath = "C:\Program Files\VideoLAN\VLC\vlc.exe"
If Not objFSO.FileExists(vlcPath) Then
    vlcPath = "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
End If

Set objShell = CreateObject("WScript.Shell")
cmd = """" & vlcPath & """ --network-caching=1500 """ & cleanUrl & """"
objShell.Run cmd, 1, False
