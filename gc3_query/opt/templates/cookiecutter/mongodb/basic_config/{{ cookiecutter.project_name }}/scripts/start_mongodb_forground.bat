@echo off
echo Starting MongoDB service

C:\tools\MongoDB\Server\3.6\bin\mongod.exe --config C:\tools\MongoDB\configs\mongo-service.config --service

echo MongoDB service started.
