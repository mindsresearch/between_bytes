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
echo "SelfScape Insight built and installed in venv!"

read -p "Do you want to build docs? (Y/n) " build_docs

if [ "$build_docs" = "$yes" ]; then
    echo "Building docs..."
    cd docs
    make html
    cd ..
    echo "Docs built!"
fi

echo "Done!"
echo "To run the program, activate the venv ($ source venv/bin/activate)"
echo "and run the CLI version ($ scape-cli) or the GUI version ($ scape-gui)"
echo "To view the docs, open docs/_build/html/index.html in a browser"
