#!/bin/sh

python3 -m venv .
source ./bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --log pip_log_$(echo $(date +%s)).log --upgrade --disable-pip-version-check --force-reinstall -r requirements.txt