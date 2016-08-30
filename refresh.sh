#! /bin/bash

if [ $1 ]
	then
	echo
	if [ -f ./.processID ]
		then
			pid=$(<.processID)	
			r=$( (sudo kill "$pid") 2>&1)
			if [ ${#r} -gt 0 ]
				then echo "Process ID error"
			fi
	fi
	echo "Starting $1 .."
	sudo python $1 &
	echo $! > ./.processID
else
	echo "Error: Missing argument. Try './refresh.sh [server file]'"
fi


