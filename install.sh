#!/bin/bash

python_version="3.6"
python_path="/usr/local/bin/python$python_version"

# Find Python install location
if [ ! -f $python_path ]; then
    echo "Python $python_version not found. Enter the path to your Python $python_version install."
    read python_path
fi

# Set up virtual environment
if virtualenv --python=$python_path python-3.6-env; then
    echo -e "\nVirtual environment configured! Installing requirements..."
else
    echo -n "Installing virtual environment failed. You must have Python $python_version installed on your system."
    exit 1
fi

pip install -r requirements.txt
mkdir secret

# Discord setup
echo -e "\nEnter your bot's Discord token: "
read token
echo $token > secret/token.txt
echo -e "\nSuccess! The bot has been installed."
