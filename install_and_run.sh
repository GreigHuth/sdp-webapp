#!/bin/bash


if [ ! -d "%HOME/sdp-webapp/.venv/bin/activate" ]
then
    virtualenv .venv/
fi
source $HOME/sdp-webapp/.venv/bin/activate
pip install -r requirements.txt
flask run
