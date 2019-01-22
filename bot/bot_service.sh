#!/bin/bash
# Run the bot and restart if it crashes

# Setup virtualenv 
source ../python-3.6-env/bin/activate

# Run bot loop
while true
do
	python3 index.py
	exit_code=$?

	if [ $exit_code -ne 0 ] 
	then 
		printf "The bot crashed with exit code $exit_code. Restarting...\n\n"
		sleep 1
	else
		printf "The bot exited gracefully. Bye!\n"
		exit
	fi
done
