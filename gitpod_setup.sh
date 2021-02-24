#!/bin/sh

export PYTHONPATH=$(pwd)
echo export PYTHONPATH=$(pwd) >> ~/.bashrc

pip install --upgrade pip

pip install --upgrade -r ./requirements.txt

python -m playwright install
