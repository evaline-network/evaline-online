# Сервисы и домены компании EVA-LINE

## Веб-сервисы
- **evabot.online** — основной сайт-платформа и чат ЕваБот (SPA, чат, голос, лицо).
- **evaline.online** — корпоративный сайт компании.
- **evaline.network** — сеть/эко-система сервисов.
- **evaline.com.ua** — продакт-сайт (зеркало в базе знаний: `knowledge-base/evaline-com-ua/site`, языки uk/en/ru/ro/de/pl).
- **business.evaline.online** — бизнес-портал (Telemetry & Status) через GCP-балансировщик; /api проксируется на бэкенд.
- **Cloud Run business-tier-api** — отдельный B2B API с тирами и биллингом.

## Публичные разделы (на evabot.online / face)
- `/face` — 3D-лицо Евы.
- `/docs` — документация.
- `/voice` — голосовые настройки (персона Eva/Adam, autosend, TTS).

## API поверхность (бэкенд :3000)
- `POST /api/chat`, `POST /api/chat/stream` — чат (unary / SSE), параметры: message, model, history, persona, lang, role, provider, apiKey, useKnowledgeBase, sessionId.
- `POST /api/consilium` — мультимодельное совещание (modes: solo, broadcast, dialogue, consilium).
- `POST /api/tts` + `/api/tts/status` — синтез речи (Cloud TTS, лимит 900 000 символов/мес, только-free политика; фолбэк edge-tts: ru→Svetlana/DmitryNeural, uk→Polina/OstapNeural, en→Aria/GuyNeural).
- `POST /api/stt` — распознавание речи.
- `/api/kb/search`, `/api/kb/docs` — поиск по базе знаний (SQLite FTS5 + память).
- `/api/status`, `/api/db`, `/api/config` — диагностика.
- `/api/api-keys`, `/api/voice`, `/api/roles`, `/api/models` и др.

## Cloud Run business-tier (B2B)
- Роуты: `/health`, `/v1/api-keys`, `/v1/api-keys/{key_id}`, `/v1/billing/checkout`, `/v1/tiers`, `/v1/usage/record`, `/v1/usage/summary`, `/v1/webhooks/stripe`.
- Все `/v1` требуют API-ключ (иначе 401 MISSING_API_KEY).
- Тиры: free (10 rpm, burst 20, 10000 daily_tokens, gemini-1.5-flash), starter, pro, enterprise.
- Stripe подключение запланировано (сейчас переменные-заглушки).

## Голос и мультимедиа
- TTS: Cloud TTS первичный; браузерный speechSynthesis фолбэк; язык ответа определяется по тексту (серверная LocalePolicy + клиентский detectLang): кириллица+іїєґ → uk-UA, иначе ru-RU, латиница → en-US.
- Стриминговая озвучка реплик целиком (чанки ≤340 символов, очередь).
- STT: микрофонный ввод с автопосылом.

## Мессенджеры
- Telegram: бот запланирован (модуль есть, `src/telegram/TelegramBot.ts`), токен НЕ настроен — при отсутствии токена в .env бот отключается с логом «Telegram bot disabled (no token)».

## Прочее
- Системные пути: бэкенд `/var/www/evabot-backend`, репозитории в `/home/evabot/evaline-online`, активные проекты `/home/evabot/Desktop/` (eva-face, eva-face-3d, eva-face-matrix, eva-hub, evaline-network, gcloud, scripts).
- Деплой: `scripts/safe-deploy.sh`, откат `scripts/rollback.sh`, мониторинг `uptime-monitor.sh` / `watchdog.sh`.