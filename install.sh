#!/bin/bash

python_version=3.6

# Set up virtual environment
if virtualenv -p python$python_version python-${python_version}-env; then
    echo -e "\nVirtual environment configured! Installing requirements..."
else
    echo -n "Installing virtual environment failed. You must have Python $python_version installed on your system."
    exit 1
fi

source python-${python_version}-env/bin/activate
pip install -r requirements.txt
mkdir bot/secret

# Discord setup
echo -e "\nEnter your bot's Discord token: "
read token
echo $token > bot/secret/token.txt
echo -e "\nSuccess! The bot has been installed."
