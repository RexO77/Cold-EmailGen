@echo off
REM Cold Mail Generator - Windows launcher.
REM Double-click this file, or run "run.bat" from cmd / PowerShell.
REM It calls run.ps1 with an execution-policy bypass so script-blocking
REM never gets in the way.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
pause
