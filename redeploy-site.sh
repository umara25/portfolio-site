#!/bin/bash

tmux kill-server

cd ~/portfolio-site

git fetch && git reset origin/main --hard

python3 -m venv python3-virtualenv

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new -d -s flaskapp 'cd ~/portfolio-site && source python3-virtualenv/bin/activate && export FLASK_APP=app && export FLASK_ENV=development && flask run --host=0.0.0.0'
