<details>
  <summary>Инструкция ручной настройки</summary>
    1. Клонируем репозиторий <br>
    2. Переходим в директорий склонированного репозитория <br>
    4. Переименовываем файл /bewise_test/src/.env_example.py в .env и при необходимости редактируем <br>
    5. Собираем контейнер с помощью команды: docker-compose up --build -d <br>
    6. Подключаемся к СУБД c помощью команды в терминале: docker exec -it postgres_bewise_local /bin/bash <br>
    7. Вводим команду: psql -U postgres -p 5444, после чего создаем базу данных: CREATE DATABASE bewise_test; <br>
    8. Перезапускаем docker контейнер: docker restart bewise_local <br>
    9. Создаем виртуальное окружение с помощью команды: python3 -m venv env <br> 
    10. Активируем виртуальное окружение: source ./env/bin/activate <br>
    11. Устанавливаем дополнительные модули с помощью команды: pip install -r requirements.txt <br>
    12. Запускаем миграцию: alembic revision --autogenerate -m "Initial" <br>
    13. Запускаем обновление заголовков: alembic upgrade head <br>
</details>

Автоматизированный процесс:
1. Клонируем репозиторий  
2. Переходим в директорий склонированного репозитория  
3. Запускаем:  
```javascript
    bash ./build.sh
```
С помощью скрипта создаются контейнеры docker, создается база данных и первоначальная миграция.  
4. При необходимости последующей миграции можно отдельно запустить:
```javascript
    bash ./run_migration.sh 
```

После сборки контейнера доступна интерактивная документация Fastapi по адресу: http://127.0.0.1:5003/docs#
Но для проверки и доступа к интерактивной документации, без сборки контейнеров, был создан сервис по адресу: https://tasks.deniko1985.ml/docs#

Примеры запросов:
1. POST /questions:
    {
        "questions_num": 0
    }
2. POST /user:
    {
        "username": "string"
    }
3. PUT /file:
    content-type:  multipart/form-data
    user_id: integer
    auth_token: string
    file: string($binary)
4. GET /record:
    record_id: string($uuid4)
    user_id: integer