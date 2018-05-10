@echo off
echo Installing MongoDB service
REM -- -"C:\tools\MongoDB\Server\3.6\bin\mongod.exe" --config C:\tools\MongoDB\configs\mongo-service.config --install
"{{ cookiecutter.mongod_bin }}" --config "{{ cookiecutter.mongodb_service_config_file }}" --install --serviceName MongoDB
echo MongoDB service installed.
echo Configuring MongoDB service for Manual startup-type
sc config "MongoDB" start=demand
echo MongoDB service configured for Manual startup
echo done.
pause
