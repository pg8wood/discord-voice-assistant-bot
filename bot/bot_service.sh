#!/bin/bash
# Run the bot and restart if it crashes
while true
do
	python3 bot.py
	exit_code=$?

	if [ $exit_code -ne 0 ] 
	then 
		printf "The bot crashed with exit code $exit_code. restarting...\n\n"
		sleep 1
	else
		printf "The bot exited gracefully. Bye!\n"
		exit
	fi
done
