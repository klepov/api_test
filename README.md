# api_test
Тестовое на создание api

## Как запустить

### Шаг первый 
Выкачать репу.
перейти в терминал с проектом

### Шаг второй
Выполнить
```
docker-compose up -d
```
```
docker exec -it container_api_test bash
```
```
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell
```

### Шаг третий (добавить hr)
- войти 0.0.0.0:80/admin
- создать пользователя 0.0.0.0/admin/api/employee/add/
- прилинковать токен к пользователю - 0.0.0.0/admin/authtoken/token/add/
- создать группу "hr" - 0.0.0.0/admin/auth/group/add/
- прилинковать созданного пользователя к группе "hr"

## Документация

### создать сотрудника

POST /employee/create/
```
{
  "name": "ivan",
  "sex": 1,
  "phone_number": "+79030008888",
  "bdate": "1990-01-01",
  "username": "ke1111111k",
  "password": "kek"
}
```
```
response 200
{
  "bdate": "1990-01-01",
  "phone_number": "+79030008888",
  "name": "ivan",
  "position_departament": null,
  "sex": 1,
  "workflow_type": 0
}
```

### изменить сотрудника
PATCH /employee/<id>/
HEADER Authorization: Token	<token>
```
{
  "name": "ivan",
  "sex": 2,
  "phone_number": "+79030008888",
  "bdate": "1990-01-01",
}
```
```
response 200
{
  "bdate": "1990-01-01",
  "phone_number": "+79030008888",
  "name": "ivan",
  "position_departament": null,
  "sex": 1,
  "workflow_type": 0
}
```


### уволить/принять сотрудника
PATCH /employee/<id>/
HEADER Authorization: Token	<token>
```
{
	"workflow_type": "1",

}
        (0, 'Не выбрано'),
        (1, 'Принят на работу'),
        (2, 'Увольнен'),

```
```
response 200
{
  "bdate": "1990-01-01",
  "phone_number": "+79030008888",
  "name": "ivan",
  "position_departament": null,
  "sex": 1,
  "workflow_type": 1
}
```



### перевести в другой отдел
PATCH /employee/<id>/
HEADER Authorization: Token	<token>
```
{
	"position_departament": "1",

}

```
```
response 200
{
  "sex": 1,
  "bdate": "1990-01-01",
  "position_departament": {
    "title": "синьор",
    "departament": {
      "title": "помидор",
      "id": 2
    },
    "id": 2
  },
  "name": "ivan",
  "phone_number": "+79030008888",
  "id": 1,
  "workflow_type": 0
}
```
