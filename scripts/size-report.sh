#!/usr/bin/env bash
# Отчёт о размере публикации (важно для мобильной загрузки по ссылке)
set -euo pipefail
total=0
printf "%-34s %10s %8s\n" "ФАЙЛ" "БАЙТ" " gzip"
printf "%s\n" "-------------------------------------------------------------------"
for f in index.html manifest.webmanifest public/icon.svg public/icon-192.png public/icon-512.png public/icon-180.png; do
  [ -f "$f" ] || continue
  b=$(wc -c < "$f" | tr -d ' ')
  if command -v gzip >/dev/null 2>&1; then gz=$(gzip -9 -c "$f" | wc -c | tr -d ' '); else gz="-"; fi
  printf "%-34s %10s %8s\n" "$f" "$b" "$gz"
  total=$((total+b))
done
printf "%s\n" "-------------------------------------------------------------------"
printf "%-34s %10s\n" "ИТОГО (без three.js с CDN)" "$total"
echo
echo "three.js 0.160 (CDN, gzip) ≈ 170 КБ — грузится один раз и кешируется браузером."
