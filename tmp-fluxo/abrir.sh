#!/bin/sh
# Mac e Linux: abre o draw.io local com o fluxo mais recente da pasta "fluxos". Precisa do python3 (já vem no Mac e na maioria dos Linux).
cd "$(dirname "$0")" || exit 1
PORTA=8765
ARQ=$(ls -t fluxos/*.drawio 2>/dev/null | head -n 1)
URL="http://localhost:$PORTA/abrir.html"
[ -n "$ARQ" ] && URL="$URL?f=$ARQ"
(sleep 1; (open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null)) &
echo "draw.io em $URL (Ctrl+C para encerrar)"
exec python3 -m http.server "$PORTA" --bind 127.0.0.1
