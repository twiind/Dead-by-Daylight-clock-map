@echo off
chcp 65001 > nul
title DBD Карты и часы
cd /d "%~dp0"

echo Установка библиотек...
pip install pillow > nul 2>&1

echo Запуск программы...
python main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ОШИБКА!
    echo ========================================
    echo.
    echo Проверьте:
    echo 1. Установлен ли Python (python --version)
    echo 2. Установите pillow вручную: pip install pillow
    echo 3. Проверьте пути к картинкам
    echo.
    pause
)