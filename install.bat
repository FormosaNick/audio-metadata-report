@echo off
SET mypath="%~dp0"
cd %mypath%
py -3 -m pip install -r requirements.txt