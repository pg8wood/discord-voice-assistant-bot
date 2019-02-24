#!/bin/bash

# Find Python install location
if ! command -v python3; then
    echo "Python 3 not found."
    exit 1
fi

pip3 install virtualenv

# Set up virtual environment
if virtualenv --python=python3 python-3-env; then
    echo -e "\nVirtual environment configured! Installing requirements..."
else
    echo -n "Installing virtual environment failed. You must have Python $python_version installed on your system."
    exit 1
fi

source ../python-3.6-env/bin/activate
pip install -r requirements.txt
mkdir bot/secret

# Discord setup
echo -e "\nEnter your bot's Discord token: "
read token
echo $token > bot/secret/token.txt
echo -e "\nSuccess! The bot has been installed."
