## Сервис рассылок писем

### Описание проекта

Проект представляет собой сервис рассылок писем на основе фреймворка Django.

Он включает в себя **frontend** и **backend** разработку.

**frontend** - визуальное отображение страниц сайта

**backend** - обработка данных с сайта, реализация рассылки писем, работа с базой данных

### Основные системные требования:

* Python 3.11
* Django 4.1.7
* PostgreSQL ^12
* Зависимости (Python) из файла requirements.txt

### Запуск проекта

1. Загрузите проект из Github в директорию, воспользовавшись командой
```
git clone git@github.com:SemenOskolkov/mailing_service.git
```

2. Перейдите в директорию проекта **mailing_service**;
```
cd mailing_service
```

3. Создайте виртуальное окружение
```
python3 -m venv env
```

4. Активируйте виртуальное окружение
```
source env/bin/activate
```
Чтобы выйти из виртуального окружения, используйте команду
```
deactivate
```

5. Установите зависимости из файла **requirements.txt**
```
pip3 install -r requirements.txt
```

6. Подключитесь к PostgeSQL и создайте базу данных для работы с сервисом

7. Создайте файл **.env** для работы с переменным окружением
```
touch .env
```

8. Заполните файл **.env**, используя шаблон из файла **.env.sample**

9. Примените миграции, используя команду
```
python3 manage.py migrate
```

10. Запустите локальный сервер
```
python3 manage.py runserver
```
для запуска приложения на определенном сервере, пропишите адрес нужного сервера
```
python3 manage.py runserver 0.0.0.0:8000
```