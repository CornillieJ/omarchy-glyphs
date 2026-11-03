#!/bin/bash

# Inserts a symbol into the focused application, mirroring
# omarchy-menu-emoji-insert's clipboard-then-paste approach.

symbol="${1:-}"
copy_pid=""

[[ -n $symbol ]] || exit

printf '%s' "$symbol" | wl-copy --type text/plain --sensitive --foreground &
copy_pid=$!

sleep 0.15
wtype -M shift -k Insert -m shift 2>/dev/null || true
sleep 0.2

kill "$copy_pid" 2>/dev/null || true
