@echo OFF
REM="""
setlocal
set PythonExe=""
set PythonExeFlags=

for %%i in (cmd bat exe) do (
    for %%j in (python.%%i) do (
        call :SetPythonExe "%%~$PATH:j"
    )
)
for /f "tokens=2 delims==" %%i in ('assoc .py') do (
    for /f "tokens=2 delims==" %%j in ('ftype %%i') do (
        for /f "tokens=1" %%k in ("%%j") do (
            call :SetPythonExe %%k
        )
    )
)
%PythonExe% -x %PythonExeFlags% "%~f0" %*
goto :EOF

:SetPythonExe
if not ["%~1"]==[""] (
    if [%PythonExe%]==[""] (
        set PythonExe="%~1"
    )
)
goto :EOF
"""

""" Oracle Public Cloud CLI main runner script """

import sys

def main():
    #import opaascli.opccli
    try:
        from opaascli import opccli        
        return opccli.main()
    except ImportError as e:
        print("'psm' command not found. Please check and update path environment variable with the correct Python installation path.")

if __name__ == '__main__':

     req_version = (3,3)
     cur_version = sys.version_info

     if cur_version >= req_version:
        main()
     else:
        print("")
        print("")
        print("Please upgrade Python to version 3.3+. If already on 3.3+ version,")
        print("please update the path environment variable with the correct Python installation path.")
        print("")
