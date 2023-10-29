#!/bin/zsh

# Перейти в папку с проектом
#cd /Users/sergejgres/MyProjects/newsletter

# Активировать виртуальное окружение и запустить функцию в файле
#poetry run python3 letters/main.py

#cd /Users/sergejgres/MyProjects/newsletter && poetry run python3 letters/main.py

/opt/homebrew/bin/poetry run python3 /Users/sergejgres/MyProjects/newsletter/manage.py runcrons
