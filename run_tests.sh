#!/bin/bash

source venv/bin/activate

if [ "$(ls -A /tests)" ]; then
   echo "Running tests"
   python3 -m pytest tests
else
   echo "No tests to run"
fi
