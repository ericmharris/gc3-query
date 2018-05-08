@echo off
echo Installing MongoDB service
"C:\tools\MongoDB\Server\3.6\bin\mongod.exe" --config C:\tools\MongoDB\configs\mongo-service.config --install
echo MongoDB service installed.
pause
