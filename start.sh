#!/bin/bash

python3 -m venv .venv

source .venv/bin/activate

pip install -q -r requirements.txt

streamlit run main.py
