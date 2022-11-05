#!/bin/bash
python3 -m venv venv
cd venv/bin
source activate
cd ../..
pip3 install -r requirements.txt