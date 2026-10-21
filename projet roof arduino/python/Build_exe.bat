@echo off

echo ==================================
echo  Observatory Server Build
echo ==================================

echo.
echo Suppression anciens builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ObservatoryServer.spec del ObservatoryServer.spec

echo.
echo Generation de l EXE...
python -m PyInstaller --onefile --name ObservatoryServer observatory_server.py

echo.
echo ==================================
echo  BUILD TERMINE
echo ==================================
echo.

pause