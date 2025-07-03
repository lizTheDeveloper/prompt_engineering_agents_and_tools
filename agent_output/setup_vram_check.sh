#!/bin/bash

# Check and install py3nvml if not installed
if ! pip show py3nvml > /dev/null 2>&1; then
    echo "py3nvml not found. Installing..."
    pip install py3nvml
else
    echo "py3nvml is already installed."
fi
