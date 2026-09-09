# EVA-LINE company infrastructure (servers, GCP, network)

## Compute nodes (Google Cloud)

### 1. Compute Node — "evabot-agent-vm"
- GCP project `evabot-agent-server` (873069440066), region europe-west3-a (Frankfurt), type c3-standard-8.
- User `evabot`. Public IP 34.159.202.82, Tailscale 100.66.98.4.
- Role: all builds, tests, heavy agents and backend microservices.
- Paths: backend `/var/www/evabot-backend`, active projects `/home/evabot/Desktop/`.

### 2. Micro Node — "evaline-micro-vm"
- Same project, region us-central1 (Iowa), type e2-micro.
- Public IP 136.114.26.252, Tailscale 100.125.200.49, SSH `evabot@100.125.200.49`.
- Role: lightweight frontend, proxying to the compute node.
- Deploy to micro-server: `/var/www/evabot-backend/deploy-sync.sh`.

## GCP projects & billing
- Main project `evabot-agent-server` (873069440066) — the only one with billing enabled.
- Auxiliary `gen-lang-client-0091776451` — Compute API not enabled.
- Billing account `016725-23E254-FD499D` ("My Billing Account"); linked only to evabot-agent-server.

## DNS & domains
- `evabot.online`, `evaline.online`, `evaline.network`, `evaline.com.ua` → 136.114.26.252 (micro-VM, Caddy).
- `business.evaline.online` → 34.49.122.75 (global HTTPS load balancer `business-lb-ip`, backend = micro-VM instance group).
- Cloud Run service: `business-tier-api-873069440066.us-central1.run.app` (us-central1, containerConcurrency 80, maxScale 10).

## Systemd services (compute node)
- `evabot-brain` — main backend (node `dist/server/server.js`, port 3000) + watchdog.
- `evabot-face` — Eva 3D face (port 8093).
- `evabot-voice` — voice service.
- `evabot-model-monitor`, `evabot-registry-sync`, `evabot-watchdog` (+ timers).

## Web platform
- nginx on compute :80 → face/voice/docs routes.
- Caddy on micro-VM: TLS termination for domains, proxy to compute :3000/:80/:8093.
- Frontend: SPA `public/index.html`, face :8093, /docs, /voice.

## LLM routing
- OmniRoute — LiteLLM proxy on compute, port 20128, key `OMNIROUTE_API_KEY`.
- Free fleet routed via OpenRouter (`OPENROUTER_API_KEY`) and omni/*.

## MCP & tooling
- Unified 21-server MCP suite (`sync-mcp`): notebooklm, filesystem, git/github, memory, sqlite (~/.mcp/sqlite.db), chrome-devtools, fetch, context7, etc.
- LSP: typescript-language-server, pyright-langserver, vscode html/css/json, marksman.