@echo off

echo MongoDB started in foreground...

echo *****  Closing this window will kill MongoDB  *****

REM -- C:\tools\MongoDB\Server\3.6\bin\mongod.exe --config C:\tools\MongoDB\configs\mongo-service.config
"C:\tools\MongoDB\Server\4.0\bin\mongod.exe" --config "C:\Users\emharris\devel\gc3-query\gc3_query\var\mongodb\config\mongo-cmd.config"


echo MongoDB service started.
