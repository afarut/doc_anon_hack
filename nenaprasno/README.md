# WEB
Эта часть кода развернута на Yandex Cloud с помощью docker по адресу: http://84.201.155.51:5000/
## Установка
```cmd
git clone https://github.com/afarut/doc_anon_hack.git
```

```cmd
cd doc_anon_hack/nenaprasno
```

## Запуск на локальном сервере
### Первым делом стоит установить Docker Desktop
### Так же стоит создать базу с помощью PostgreSQL и свертиться с конфигурацией внутри .env и config.py
### Проверка работоспособности
```cmd
docker-compose build
```
```cmd
docker-compose up
```
### Выполните миграции
```cmd
docker-compose exec web bash
flask db init
flask db migrate -m "migration"
flask db upgrade
```
### Готово! Теперь сайт работает по адресу http://127.0.0.1:5000/ или тому, который вы указали в конфигурации
