@echo off
echo Installing MongoDB service
REM -- -"C:\tools\MongoDB\Server\3.6\bin\mongod.exe" --config C:\tools\MongoDB\configs\mongo-service.config --install
"{{ cookiecutter.mongod_bin }}" --config "{{ cookiecutter.mongodb_config_file }}" --install
echo MongoDB service installed.
pause
