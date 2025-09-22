# Инструкции по запуску приложения
### Первый старт (с билдом)
- docker compose up -d --build
### Проверка логов
- docker compose logs -f имя сервиса

### Swagger 
- http://localhost:8000/docs
![Фото главной страницы](images/Swagger.png)
### pgAdmin 
- http://localhost:5050 логин пароль из .env 
(Добавьте сервер: Host=db, Port=5432, User/Password — как в .env)
![Фото главной страницы](images/pgAdmin_register.png)
![Фото главной страницы](images/pgAdmin.png)
### Prometeus
- http://localhost:9090
![Фото главной страницы](images/Prometeus.png)
### Grafana
- http://localhost:3000 (admin, admin по дефолту)
![Фото главной страницы](images/Grafana.png)
### Миграции БД (alembic)
- docker compose exec api alembic upgrade head

### Стоп без удаления данных
docker compose down
### Полная очистка со всеми томами (включая кэш модели!)
docker compose down -v --remove-orphans