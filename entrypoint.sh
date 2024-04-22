#!/bin/bash

echo "Sleeping for Kafka to start"
# sleep 15s
echo "Done sleeping, continuing" 

# Check if the SCRIPT environment variable is set
if [ -z "$SCRIPT" ]; then
    echo "Error: SCRIPT environment variable is not set."
    exit 1
fi

# Check if the specified script file exists
if [ ! -f "/src/$SCRIPT.py" ]; then
    echo "Error: File '/src/$SCRIPT.py' does not exist."
    exit 1
fi

echo "Checks passed. Starting script"

# Run the specified Python script
python3 -u "/src/$SCRIPT.py"