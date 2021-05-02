#!/bin/sh

export PATH="~/.poetry/bin:$PATH"

export PIP_USER=false

poetry install

poetry run playwright install

poetry run pytest
