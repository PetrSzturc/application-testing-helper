#!/bin/sh

pip install --upgrade pip

pip install --upgrade -r ./requirements.txt

python -m playwright install
