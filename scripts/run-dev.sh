#!/usr/bin/env bash
set -o errexit

app="/SanicExample/backend"
venv="${app}/venv"

echo "Installing dependencies"
python3 -m pip install --upgrade pip
pip3 install -r "${app}/requirements.txt" -i "https://pypi.tuna.tsinghua.edu.cn/simple"

echo "Starting Sanic development server"
python3 "${app}/routes/app.py"
