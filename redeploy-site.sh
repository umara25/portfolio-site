#!/bin/bash

tmux kill-server

cd portfolio-site

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new -d -s redeploy-portfolio 'cd portfolio-site && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'
