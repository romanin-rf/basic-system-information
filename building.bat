@echo off
cls
title Building bsi_rus.py
echo ----------------------------------------------------
echo Building bsi_rus.py
echo ----------------------------------------------------
pyinstaller -F -w -i "icon.ico" bsi_rus.py
title Building bsi_eng.py
echo ----------------------------------------------------
echo Building bsi_eng.py
echo ----------------------------------------------------
pyinstaller -F -w -i "icon.ico" bsi_eng.py
title Building is done
echo ----------------------------------------------------
echo Done!!!
echo ----------------------------------------------------
pause