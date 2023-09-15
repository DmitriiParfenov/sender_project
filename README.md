# sender_project

Sender_project — это онлайн-сервис, где пользователи могут создавать клиентов и рассылки, отправлять рассылки с заданной
периодичностью, удалять их, авторизовываться по email с верификацией, сбрасывать пароль при необходимости или изменять
его в личном кабинете. Также добавлен функционал по созданию статей. При количестве просмотров выше 100 на указанную
пользователем почту приходит сообщение с поздравлением.
Сайт написан на Python с использованием Django для запросов пользователя и Bootstrap для frontend. 
Работа с изображениями — pillow. База данных — PostgreSQL.

# Дополнительная информация

- Для создания суперпользователя из директории `sender_project` выполните в консоли: </br>
```
python manage.py csu
```
- Для создания группы `Manager` с правами для просмотра всех пользователей и рассылок, а также для отключения
любых рассылок и пользователей, из директории `sender_project` выполните в консоли: </br>
```
python manage.py cmg
```
- Для отправки рассылок из директории `sender_project` выполните в консоли: </br>
```
python manage.py start_cron
```

# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/sender_project.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/sender_project.git
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```
# Установка и настройка Redis

- Установите Redis, если он не установлен. Для этого выполните в консоли:
```
sudo apt install redis-server
``` 
- Запустите Redis, выполнив в консоли:
```
sudo service redis-server start
``` 
- Произойдет запуск Redis сервера на порту 6379. Для того, чтобы убедиться, что сервер запущен, необходимо выполнить
в консоли команду, ответом которой должен быть `PONG`.
```
redis-cli ping
```

# Работа с базой данной PostgreSQL

- Установите PostgreSQL, если он не установлен. Для этого, например для Ubuntu, выполните в консоли:
```
sudo apt install postgresql
```
- Выполните вход в интерактивную оболочку PostgreSQL от имени `postgresql`, выполнив в консоли:
```
sudo -i -u postgres psql
```
- Создайте базу данный для проекта, выполнив в консоли:
```
CREATE DATABASE sender_project;
```
- Закройте интерактивную оболочку PostgreSQL:
```
\q
```

# Работа с переменными окружения

- В директории `sender_project` создайте файл `.env`. Пример содержимого файла:
```
EMAIL_BACKEND=путь импорта Python для вашего класса бэкенда
EMAIL_HOST=хост SMTP
EMAIL_HOST_USER=адрес электронной почты для аутентификации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутентификации на почтовом сервере

CACHE_ENABLED=1

LOCATION=местоположение используемого кеша (redis)
```

# Настройка Django-crontab в подсистеме Linux (wsl)

- Добавьте команду в crontab, выполнив в консоли:
```
python manage.py crontab add
``` 
- Запустите cron, выполнив в консоли:
```
sudo service cron start
``` 
- Включите текущего пользователя `windows` в группу cron:
```
sudo usermod -a -G crontab (username)
```     

# Работа с миграциями

Из директории `sender_project` выполните в консоли: </br>

```
python manage.py migrate
```

# Запуск сервера Django

- Активируйте виртуальное окружение согласно п. `Клонирование репозитория` </br>

- Из  директории `sender_project` выполните в консоли: </br>
```
python manage.py runserver
```  
или 
```
python3 manage.py runserver
```
