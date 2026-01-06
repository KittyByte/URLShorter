# URLShorter 
Сервис по сокращению ссылок


### 1. Подготовка проекта и инфраструктура (обязательно сначала)
- [ ] Добавить базовый CI (GitHub Actions: lint + tests)

### 2. MVP: Core функциональность сокращателя
- [ ] Реализовать модель ссылки в MongoDB (pymongo или motor для async)
- [ ] Эндпоинт POST /shorten (анонимный на первом этапе)
  - Валидация URL через pydantic
  - Генерация короткого кода (base62 от counter или hash)
  - Проверка коллизий
  - Сохранение в Mongo
  - Кэширование в Redis (SET short_code -> original_url с TTL)
- [ ] Эндпоинт GET /{short_code}
  - Сначала проверка в Redis
  - Если miss — загрузка из Mongo и заполнение Redis
  - 301 Redirect на original_url
  - Если не найдено — 404 с красивой страницей
- [ ] Добавить BackgroundTask для асинхронного логирования клика (пока просто в лог или временную коллекцию)

### 3. Аутентификация и пользователи
- [ ] Подключить PostgreSQL + SQLAlchemy + Alembic
- [ ] Создать модель User (id, username, email, password_hash)
- [ ] Миграции через Alembic
- [ ] Реализовать регистрацию и логин (JWT или FastAPI Users)
- [ ] Защитить эндпоинты Depends(get_current_user)
- [ ] Привязать короткие ссылки к user_id в MongoDB
- [ ] Эндпоинт GET /my-links — список ссылок пользователя (пагинация)

### 4. Метрики и аналитика (самая интересная часть твоего стека)
- [ ] Подключить ClickHouse (драйвер clickhouse-driver или async-clickhouse)
- [ ] Создать таблицу clicks (short_code, timestamp, ip, user_agent, referrer, country?)
- [ ] В BackgroundTask при редиректе — асинхронная вставка в ClickHouse
- [ ] Эндпоинт GET /stats/{short_code} (только для владельца или публично?)
  - total_clicks
  - clicks_by_day (GROUP BY date)
  - unique_ips
  - top_referrers
  - топ стран (если добавишь geo)
- [ ] (Опционально) Materialized Views в ClickHouse для предрасчёта ежедневных статистик
- [ ] (Nice-to-have) Парсинг user_agent (библиотека user-agents) → device/browser/os
- [ ] (Nice-to-have) GeoIP (MaxMind GeoLite2 локально) → country/city

### 5. Безопасность и защита от abuse
- [ ] Rate limiting (с Redis): лимит на создание ссылок по IP/user_id
- [ ] Валидация и санитизация всех входных данных
- [ ] Защита от SSRF (проверка, что original_url не внутренний IP)
- [ ] Опциональная экспирация ссылок (expires_at поле)

### 6. Дополнительные фичи (для senior-уровня и портфолио)
- [ ] Кастомные алиасы (POST /shorten с optional custom_code, проверка уникальности)
- [ ] Генерация QR-кодов (библиотека qrcode, эндпоинт /qr/{short_code})
- [ ] Удаление/редактирование ссылок (только владельцем)
- [ ] Публичная статистика (опционально выключить для приватных ссылок)
- [ ] Webhooks на новые клики (очередь в Redis + Celery worker)

### 7. Тестирование и качество кода
- [ ] Написать unit-тесты (pytest + httpx для API)
- [ ] Интеграционные тесты с тестовой БД/Redis
- [ ] Достичь coverage > 80%
- [ ] Добавить типизацию (mypy strict)

### 8. Деплой и мониторинг
- [ ] Dockerfile для продакшена
- [ ] Настроить Swagger / Redoc (уже есть в FastAPI)
- [ ] (Опционально) Prometheus metrics + Grafana
- [ ] Задеплоить (Render, Fly.io, VPS или Railway)

### Рекомендация по порядку
1. Сначала этапы 1–2 → у тебя будет работающий сокращатель за пару дней.
2. Потом этап 3 (auth) → проект становится персонализированным.
3. Затем этап 4 (ClickHouse + метрики) → самая ценная часть.
4. Остальное — по желанию и времени.
