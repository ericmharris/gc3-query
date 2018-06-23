# .bashrc
################################################################################
###  Bash RC File
################################################################################
# 0644 permissions

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# User specific aliases and functions
set -o vi
export GREP_OPTIONS='--color=auto'

alias sd='sudo su - '

alias ll='ls -l'
alias llh='ls -lh'


alias gadd='git add -A'
alias gcomm='git commit -a'
alias gstat='git status'
alias gpull='git pull origin master'
alias gpush='git push origin master'
alias gpush='git push origin master'


timestamp ()
{
# 04_25_2018.15_55_28
	# date +%m_%d_%Y.%H_%M_%S
	# date +%Y%m%dT%H%M%S
	# 2018_06_19T132208
	# date +%Y_%m_%dT%H%M%S
	# 2018_06_19T13.22.35
	date +%Y_%m_%dT%H.%M.%S
}

datestamp ()
{
# 04_25_2018
	date +%m_%d_%Y
}

alias ts='timestamp'
alias ds='datestamp'


py36 ()
{
alias python='python3.6'
alias python3='python3.6'
alias pip='pip3.6'
alias pip3='pip3.6'
}
