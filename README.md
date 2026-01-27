# URLShorter 
Сервис по сокращению ссылок


### 3. Аутентификация и пользователи
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

