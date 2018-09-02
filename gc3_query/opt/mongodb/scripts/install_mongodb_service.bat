@echo off
echo Installing MongoDB service
REM -- -"C:\tools\MongoDB\Server\3.6\bin\mongod.exe" --config C:\tools\MongoDB\configs\mongo-service.config --install
"C:\tools\MongoDB\Server\4.0\bin\mongod.exe" --config "C:\Users\emharris\devel\gc3-query\gc3_query\var\mongodb\config\mongo-service.config" --install --serviceName MongoDB
echo MongoDB service installed.
echo Configuring MongoDB service for Manual startup-type
sc config "MongoDB" start=demand
echo MongoDB service configured for Manual startup
echo done.
pause
