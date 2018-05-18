@echo off
echo Configuring KiTTY to store configuration in: {{ cookiecutter.home_directory }}\{{ cookiecutter.kitty_home_dir_name }}
REM -- cp {{ cookiecutter.home_directory }}\{{ cookiecutter.kitty_home_dir_name }}\kitty.ini {{ cookiecutter.kitty_bin_dir }}
REM -- {{ cookiecutter.kitty_bin }} -convert-dir

cp {{ cookiecutter.home_directory }}\{{ cookiecutter.kitty_home_dir_name }}\kitty.ini {{ cookiecutter.kitty_bin_dir }}
{{ cookiecutter.kitty_bin }} -convert-dir

echo KiTTY Configured for dir-mode
echo done.
pause
