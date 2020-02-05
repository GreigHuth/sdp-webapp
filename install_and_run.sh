#!/bin/bash

virtualenv .venv/
source $HOME/sdp-webapp/.venv/bin/activate
pip install -r requirements.txt
python app.py
