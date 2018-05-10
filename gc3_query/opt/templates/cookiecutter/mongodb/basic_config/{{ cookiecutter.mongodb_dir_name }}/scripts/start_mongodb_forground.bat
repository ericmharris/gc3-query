@echo off
echo Starting MongoDB service

REM -- C:\tools\MongoDB\Server\3.6\bin\mongod.exe --config C:\tools\MongoDB\configs\mongo-service.config --service
"{{ cookiecutter.mongod_bin }}" --config "{{ cookiecutter.mongodb_config_file }}"  --service


echo MongoDB service started.
