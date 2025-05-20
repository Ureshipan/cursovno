#!/bin/bash

# Проверяем наличие python3-venv
if ! dpkg -l | grep -q python3-venv; then
    echo "Установка python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
fi

# Проверяем наличие venv
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "Активация виртуального окружения..."
source venv/bin/activate

# Проверяем наличие requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Проверка и установка зависимостей..."
    pip install -r requirements.txt
fi

# Запускаем программу
echo "Запуск программы..."
python3 openfoam_gui.py

# Деактивируем виртуальное окружение при выходе
deactivate
