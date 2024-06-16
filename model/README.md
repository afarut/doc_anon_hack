# Запуск нашего решения

```cmd
docker build -t girya_team .
```

```cmd
docker run -p 5000:5000 girya_team
```

# Запросы

## Проверка работоспособности
```
curl -H "Content-type: application/json" -X GET http://localhost:5000
```

## Запрос в модель
```
curl -H "Content-type: application/json" -X POST -d '{"text": "Текстовое сообщение. Не более 512 символов за один запрос."}' http://localhost:5000
```
