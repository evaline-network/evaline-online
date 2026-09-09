# Инфраструктура компании EVA-LINE (серверы, GCP, сеть)

## Вычислительные узлы (Google Cloud)

### 1. Compute Node — «evabot-agent-vm»
- GCP проект: `evabot-agent-server` (номер 873069440066), регион europe-west3-a (Франкфурт).
- Тип: c3-standard-8. Пользователь: `evabot`.
- Публичный IP: 34.159.202.82. Tailscale IP: 100.66.98.4.
- Роль: все сборки, тесты, тяжёлые агенты и бэкенд-микросервисы.
- Пути: веб-бэкенд `/var/www/evabot-backend`, активные проекты в `/home/evabot/Desktop/`.

### 2. Micro Node — «evaline-micro-vm»
- Тот же GCP проект, регион us-central1 (Айова). Тип: e2-micro.
- Публичный IP: 136.114.26.252. Tailscale IP: 100.125.200.49. SSH: `evabot@100.125.200.49`.
- Роль: лёгкий фронтенд и проксирование на compute-узел.
- Кэш/Tailscale распределяются автоматически; деплой на микро-сервер: `/var/www/evabot-backend/deploy-sync.sh`.

## GCP-проекты и биллинг
- Основной проект: `evabot-agent-server` (873069440066) — единственный с включённым биллингом.
- Вспомогательный: `gen-lang-client-0091776451` — Compute API не включён.
- Billing аккаунт: `016725-23E254-FD499D` («My Billing Account»); привязан только evabot-agent-server.

## DNS и домены
- `evabot.online`, `evaline.online`, `evaline.network`, `evaline.com.ua` → 136.114.26.252 (micro-VM, Caddy).
- `business.evaline.online` → 34.49.122.75 (глобальный HTTPS-балансировщик GCP `business-lb-ip`, бэкенд — instance group микро-VM; проксирует на содержание бизнес-портала и /api).
- Cloud Run сервис: `business-tier-api-873069440066.us-central1.run.app` (us-central1, containerConcurrency 80, maxScale 10).

## Системные сервисы (systemd на compute-узле)
- `evabot-brain` — основной бэкенд (node `dist/server/server.js`, порт 3000). + watchdog.
- `evabot-face` — 3D-лицо Евы (порт 8093).
- `evabot-voice` — голосовой сервис.
- `evabot-model-monitor`, `evabot-registry-sync`, `evabot-watchdog` (+ таймеры).

## Веб-платформа
- nginx на compute: порт 80 → face/voice/docs на микро-маршруты.
- Caddy на микро-VM: терминация TLS для доменов, прокси на compute :3000 / :80 / :8093.
- Фронтенд: SPA `public/index.html` (128 КБ, статика), лицо :8093, /docs, /voice.

## LLM-маршрутизация
- OmniRoute — LiteLLM-прокси на compute: порт 20128, ключ — `OMNIROUTE_API_KEY`.
- Фрифлот маршрутизируется через OpenRouter (`OPENROUTER_API_KEY`) и omni/*.

## MCP и инструменты
- Единый MCP-комплект из 21 сервера (`sync-mcp`): notebooklm, filesystem, git/github, memory, sqlite (~/.mcp/sqlite.db), chrome-devtools, fetch, context7 и др.
- LSP: typescript-language-server, pyright-langserver, vscode html/css/json, marksman.