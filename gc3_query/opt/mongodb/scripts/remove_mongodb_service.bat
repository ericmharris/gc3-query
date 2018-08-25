@echo off
echo Installing MongoDB service
REM -- -"C:\tools\MongoDB\Server\3.6\bin\mongod.exe" --config C:\tools\MongoDB\configs\mongo-service.config --install
"C:\tools\MongoDB\Server\4.0\bin\mongod.exe" --config "C:\Users\emharris\devel\gc3-query\gc3_query\var\mongodb\config\mongo-service.config" --remove --serviceName MongoDB
echo MongoDB service removed.
echo done.
pause
