#!/bin/bash

tmux kill-session

cd mlh-portfolio-site

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

deactivate

cd ..

tmux new -d -s portfolio

tmux send-keys -t portfolio "
cd mlh-portfolio-site
source python3-virtualenv/bin/activate
flask run --host=0.0.0.0
" C-m