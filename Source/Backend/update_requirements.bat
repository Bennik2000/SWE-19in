@echo off

call .venv\Scripts\activate
call venv\Scripts\activate

pip install -r requirements.txt

call deactivate

pause