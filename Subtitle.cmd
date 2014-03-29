@echo off
cls
set PATH=%PATH%;C:\Python27\
:MY_LOOP
IF %1=="" GOTO EXIT_LOOP

S:\Personal\SubDown\dist\subtitle-downloader.exe %1 
SHIFT
GOTO MY_LOOP

:EXIT_LOOP
echo "Done as you Demanded!"

