@echo off

rem Create venv
python -m venv .venv
call .venv\Scripts\activate

rem Install requirements
pip install -r requirements.txt
