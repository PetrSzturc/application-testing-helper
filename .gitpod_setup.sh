#!/bin/sh

poetry install

poetry run playwright install

poetry run pytest
