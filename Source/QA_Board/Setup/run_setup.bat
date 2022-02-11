:: replace postgres with your username adn default with your password for postgreSQL
@echo off
%~dp0\..\venv\Scripts\python.exe %~dp0\setup_dbs.py postgres default
pause