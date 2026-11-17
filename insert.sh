#!/bin/bash

# Inserts a symbol into the focused application, mirroring
# omarchy-menu-emoji-insert's clipboard-then-paste approach.

symbol="${1:-}"
copy_pid=""

[[ -n $symbol ]] || exit

printf '%s' "$symbol" | wl-copy --type text/plain --sensitive --foreground &
copy_pid=$!

sleep 0.15

# Firefox ignores a synthetic Shift+Insert, terminals do not paste on Ctrl+V
window_class=$(hyprctl activewindow -j | jq -r '.class')
if [[ $window_class =~ ^(foot|Alacritty|kitty|com\.mitchellh\.ghostty)$ ]]; then
  wtype -M shift -k Insert -m shift 2>/dev/null || true
else
  wtype -M ctrl -k v -m ctrl 2>/dev/null || true
fi

sleep 0.2

kill "$copy_pid" 2>/dev/null || true
