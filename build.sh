#!bin/bash

yes="Y"

read -p "Do you want to remove an existing build? (removes dirs venv and dist) (Y/n) " remove
if [ "$remove" = "$yes" ]; then
    rm -r venv
    rm -r dist
fi

echo "Creating virtual environment..."
virtualenv venv

echo "Building and installing..."
flit install --python venv/bin/python3


echo "SelfScape Insight installed in venv!"