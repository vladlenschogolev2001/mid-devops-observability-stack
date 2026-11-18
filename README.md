# Observability Stack — Middle DevOps Project

Полный стек наблюдаемости (Observability) уровня Middle DevOps.

## Что внутри

- **Prometheus** — сбор метрик
- **Grafana** — дашборды и визуализация
- **Loki** — агрегация логов
- **Alertmanager** — алертинг
- **Sample App** с метриками и логами
- **Docker Compose** для локального запуска одной командой
- Готовые дашборды и алерты

## Архитектура

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Sample App │────▶│  Prometheus  │────▶│   Grafana   │
│  (metrics)  │     │              │     │  (dashboards)│
└──────┬──────┘     └──────┬───────┘     └─────────────┘
       │                   │
       │ logs              │ alerts
       ▼                   ▼
┌─────────────┐     ┌──────────────┐
│    Loki     │     │ Alertmanager │
└─────────────┘     └──────────────┘
```

## Быстрый старт

### Запуск всего стека

```bash
docker compose up -d
```

### Доступ

| Сервис        | URL                      | Логин / Пароль     |
|---------------|--------------------------|--------------------|
| Grafana       | http://localhost:3000    | admin / admin123   |
| Prometheus    | http://localhost:9090    | —                  |
| Alertmanager  | http://localhost:9093    | —                  |
| Sample App    | http://localhost:8000    | —                  |
| Loki          | http://localhost:3100    | —                  |

### Остановка

```bash
docker compose down -v
```

## Что показывает этот проект (Middle level)

- Полноценный observability stack
- Service discovery и scrape configs
- Recording rules + Alerting rules
- Grafana provisioning (datasources + dashboards as code)
- Structured logging → Loki
- Alertmanager routing
- Docker Compose multi-service orchestration
- Healthchecks и restart policies

## Структура

```
03-observability-stack/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml
│   ├── rules/
│   │   └── alerts.yml
│   └── recording_rules.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   └── dashboards/
│   └── dashboards/
├── loki/
│   └── loki-config.yml
├── alertmanager/
│   └── alertmanager.yml
├── app/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
└── scripts/
    └── generate-load.sh
```

## Полезные запросы

### Prometheus

```promql
# RPS
rate(http_requests_total[1m])

# Latency p95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

### LogQL (Loki)

```logql
{job="sample-app"} |= "error"
{job="sample-app"} | json | level="ERROR"
```

## Лицензия

MIT
