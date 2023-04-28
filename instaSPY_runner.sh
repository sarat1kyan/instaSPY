#!/bin/bash

echo "here we go..."

banner1() {
  local text="$@"
  local length=$(( ${#text} + 2 ))
  local line=$(printf '%*s' "$length" '' | tr ' ' '-')
  echo "+$line+"
  printf "| %s |\n" "$(date)"
  echo "+$line+"
  printf "|$bold%s$reset|\n" "$text"
  echo "+$line+"
}

# Check if script is being run as root
if [[ $EUID -ne 0 ]]; then
  banner1 "This script may be run as root."
  exit 1
fi

#clolors
white='\e[1;37m'
green='\e[0;32m'
blue='\e[1;34m'
red='\e[1;31m'
yellow='\e[1;33m' 
echo ""
echo ""
banner() {
	echo -e $'\e[1;33m\e[0m\e[1;37m      ██▓ ███▄    █   ██████ ▄▄▄█████▓ ▄▄▄        ██████  ██▓███ ▓██   ██▓    \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m     ▓██▒ ██ ▀█   █ ▒██    ▒ ▓  ██▒ ▓▒▒████▄    ▒██    ▒ ▓██░  ██▒▒██  ██▒    \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m     ▒██▒▓██  ▀█ ██▒░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░    \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m     ░██░▓██▒  ▐▌██▒  ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██   ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░    \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m     ░██░▒██░   ▓██░▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░    \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m     ░▓  ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒     \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m      ▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░    ░      ▒   ▒▒ ░░ ░▒  ░ ░░▒ ░     ▓██ ░▒░     \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m      ▒ ░   ░   ░ ░ ░  ░  ░    ░        ░   ▒   ░  ░  ░  ░░       ▒ ▒ ░░      \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m            ░     ░       ░       ░         ░ ░   ░       ░                   \e[0m'
	echo -e $'\e[1;33m\e[0m\e[1;37m                          ░                       ░                           \e[0m'
	
	
	echo""    
	echo -e $'\e[1;33m\e[0m\e[1;33m    ██████████\e[0m'"\e[96m██████████"'\e[1;33m\e[0m\e[1;31m██████████\e[0m' '\e[1;32m\e[0m\e[1;32m grant root privileges on your android device with sudroid \e[0m''\e[1;37m\e[0m\e[1;37m \e[0m'                                       
	echo ""
	echo -e $'\e[1;33m\e[0m\e[1;33m  [ \e[0m\e[1;32m Follow on Github :- https://github.com/54R4T1KY4N \e[0m \e[1;32m\e[0m\e[1;33m] \e[0m'
	echo ""
	echo -e $'\e[1;37m\e[0m\e[1;37m    +-+-+-+-+-+-+-+ >>\e[0m'
	echo -e "\e[93m    suDROID |3|.|2| stable"      
	echo -e $'\e[1;37m\e[0m\e[1;37m    +-+-+-+-+-+-+-+ >>\e[0m' 
	echo ""                                                
}
banner 

# Check for package manager
if command -v apt-get &> /dev/null
then
    echo "Using apt package manager"
    sudo apt-get update
    sudo apt-get install -y python3-pip
elif command -v yum &> /dev/null
then
    echo "Using yum package manager"
    sudo yum update
    sudo yum install -y python3-pip
elif command -v pacman &> /dev/null
then
    echo "Using pacman package manager"
    sudo pacman -Syu python-pip
elif command -v dnf &> /dev/null
then
    echo "Using dnf package manager"
    sudo dnf update
    sudo dnf install -y python3-pip
elif command -v zypper &> /dev/null
then
    echo "Using zypper package manager"
    sudo zypper refresh
    sudo zypper install -y python3-pip
else
    echo "Unsupported package manager. Please install python3-pip manually and run the script again."
    exit 1
fi

# Install required packages
sudo pip3 install -r requirements.txt

# Run the Python script
python3 instaSPY_engine.py