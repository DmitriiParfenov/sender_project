# sender_project

Sender_project — это онлайн-сервис, где пользователи могут создавать клиентов и рассылки, отправлять рассылки с заданной
периодичностью, удалять их, авторизовываться по email с верификацией, сбрасывать пароль при необходимости или изменять
его в личном кабинете. Также добавлен функционал по созданию статей. При количестве просмотров выше 100 на указанную
пользователем почту приходит сообщение с поздравлением.
Сайт написан на Python с использованием Django для запросов пользователя и Bootstrap для frontend. 
Работа с изображениями — pillow. База данных — PostgreSQL.

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



# Работа с переменными окружения

- Установите адрес электронный почты [yandex](https://mail.yandex.ru/) в переменную окружения: `yandex_login`.
- Установите пароль для работы с приложением SMTP [yandex](https://id.yandex.ru/security/app-passwords) в переменную окружения: `yandex_password_smtp`.
- Установите пароль для работы с базой данных `postgresql` для пользователя `postgres` в переменную окружения: `password`.

# Запуск

Выполните в консоли: </br>

```
python manage.py runserver
```