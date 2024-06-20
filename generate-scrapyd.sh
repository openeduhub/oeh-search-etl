#!/bin/bash
python3 -m venv venv_scrapyd
# activating the venv:
source ./venv_scrapyd/bin/activate
# confirm that you are within your venv, then install the scrapyd-client:
pip3 install scrapyd-client