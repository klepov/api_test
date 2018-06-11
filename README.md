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
