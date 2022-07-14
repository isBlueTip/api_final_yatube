# REST API для соцсети Yatube

## Описание

REST API для взаимодействия с соцсетью Yatube. Позволяет получить доступ к ресурсам Yatube с любого устройства, используя авторизацию через JWT. Для доступа к моделям применены вьюсеты

## Установка проекта локально

Установите зависимости из requirements.txt и в папке склонированного репозитория выполните:

```bash
cd yatube_api
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --email admin@admin.com --username admin -v 3
```
Задайте пароль для суперпользователя. Логин суперпользователя - admin.  
Запустите тестовый сервер командой
```Bash
python3 manage.py runserver
```
Для проверки работоспособности, перейдите на /admin


## Заполнение БД тестовыми данными

```bash
python3 manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
exit()
python3 manage.py loaddata ../fixtures/fixtures.json
```

## Документация API

Доступна по адресу /redoc при развёрнутом проекте

## Стек

Django, Django REST framework, JWT, Redoc, SQL

## Автор

Семён Егоров  


[LinkedIn](https://www.linkedin.com/in/simonegorov/)  
[Email](rhinorofl@gmail.com)  
[Telegram](https://t.me/SamePersoon)
