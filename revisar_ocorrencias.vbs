Dim objShell
Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c C:\Users\Jorge\gestao_ocorrencias\venv\Scripts\python.exe C:\Users\Jorge\gestao_ocorrencias\manage.py revisar_ocorrencias", 0, False
Set objShell = Nothing
