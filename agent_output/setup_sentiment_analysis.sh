#!/bin/bash

# This script sets up the environment for the sentiment analysis program

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Upgrade pip
echo 'Upgrading pip...'
pip install --upgrade pip

# Install required packages
echo 'Installing required packages...'
pip install nltk matplotlib

echo 'Setup complete. To run the program, use: source env/bin/activate && python sentiment_analysis.py'