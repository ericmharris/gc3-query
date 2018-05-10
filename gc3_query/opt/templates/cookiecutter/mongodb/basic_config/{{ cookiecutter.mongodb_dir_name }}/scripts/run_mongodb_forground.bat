@echo off

echo MongoDB started in foreground...

echo *****  Closing this window will kill MongoDB  *****

REM -- C:\tools\MongoDB\Server\3.6\bin\mongod.exe --config C:\tools\MongoDB\configs\mongo-service.config
"{{ cookiecutter.mongod_bin }}" --config "{{ cookiecutter.mongodb_cmd_config_file }}"


echo MongoDB service started.
