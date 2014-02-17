@echo off
cls
set PATH=%PATH%;C:\Python27\
:MY_LOOP
IF %1=="" GOTO EXIT_LOOP

python S:\SubDown\subtitle-downloader.py %1 
SHIFT
GOTO MY_LOOP

:EXIT_LOOP


