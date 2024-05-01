#!/bin/sh
#Check weather file exists
echo "Welcome to WDCAutomete!"

#Check if both env variables hour and minute are set
if [ -z $HOUR ] && [ -z $MINUTE ]; then
    echo "Both HOUR and MINUTE env variables are not set."
    exit "Please set the HOUR and MINUTE env variables in the docker config"
fi

echo "Waiting for $HOUR:$MINUTE to start WDCAutomete"

#Wait for the time to be the same as the time set in the env variables
while true; do
    if [ $(date +"%H") -eq $HOUR ] && [ $(date +"%M") -eq $MINUTE ]; then
        echo "$HOUR:$MINUTE time reached. Starting WDCAutomete"
        python3 /app/src/main.py

        #Kill any stray firefox processes
        pkill -f firefox
    fi
    sleep 60
done