#!/bin/bash
# Генерация нагрузки для демонстрации метрик и алертов

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
DURATION="${2:-60}"   # секунд
RPS="${3:-10}"        # примерный RPS

echo "Generating load against $BASE_URL for ${DURATION}s (~${RPS} RPS)"
echo "Press Ctrl+C to stop early"

END=$((SECONDS + DURATION))

while [ $SECONDS -lt $END ]; do
  # Основной трафик
  curl -s -o /dev/null "$BASE_URL/api/data" &
  curl -s -o /dev/null "$BASE_URL/" &
  
  # Иногда медленный эндпоинт
  if (( RANDOM % 10 == 0 )); then
    curl -s -o /dev/null "$BASE_URL/api/slow" &
  fi

  # Контроль RPS
  sleep $(echo "1/$RPS" | bc -l)
done

wait
echo "Done."
