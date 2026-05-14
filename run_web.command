#!/bin/zsh
set -e

cd "$(dirname "$0")"

cleanup() {
  if [[ -n "$BACKEND_PID" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

.venv/bin/python backend.py &
BACKEND_PID=$!

cd web
npm run dev
