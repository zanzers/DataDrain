Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\workspace\DataDrain"
WshShell.Run """E:\workspace\DataDrain\.venv\Scripts\pythonw.exe"" ""E:\workspace\DataDrain\ui.py""", 0, False