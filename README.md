# api_test
Тестовое на создание api

## Как запустить

### Шаг первый 
Выкачать репу.
перейти в терминал с проектом

### Шаг второй
Выполнить
```
- docker-compose up -d
```
```
- docker exec -it container_api_test bash
```
```
- echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell
```

### Шаг третий (добавить hr)
- войти 0.0.0.0:80/admin
- создать пользователя 0.0.0.0/admin/api/employee/add/
- прилинковать токен к пользователю - 0.0.0.0/admin/authtoken/token/add/
- создать группу "hr" - 0.0.0.0/admin/auth/group/add/
- прилинковать созданного пользователя к группе "hr"
