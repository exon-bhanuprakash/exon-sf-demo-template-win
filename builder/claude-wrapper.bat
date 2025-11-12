@echo off
REM Claude Code CLI Wrapper for Windows
REM Uses Python wrapper to handle claude.cmd execution properly
REM %~dp0 is the directory containing this .bat file (builder\)

"%~dp0venv\Scripts\python.exe" "%~dp0claude-wrapper.py" %*
