#!/usr/bin/env bash
#
# Replace the placeholder plates in images/ with real stock photos.
#
# The site was built inside a sandbox whose network policy blocks Unsplash,
# Pexels and every other photo CDN, so the repo ships with generated
# placeholder plates instead. Run this on any machine with normal internet
# access and it will swap in real photos under the same filenames — no HTML
# or CSS changes needed.
#
#   bash tools/fetch-stock-images.sh
#
# How it works: it scrapes each Unsplash search page for genuine
# images.unsplash.com photo IDs (never invented ones), downloads the first
# unused match per slot, then verifies the file is a real JPEG over 30KB.
# Anything that fails verification is reported and the placeholder is kept.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
mkdir -p images
BACKUP="images/_placeholders-backup"
mkdir -p "$BACKUP"

# slot|unsplash search term|width
# NOTE: service-remodel.jpg and service-repair.jpg are deliberately absent —
# they already hold images the client chose (see IMAGES-NEEDED.md). Do not add
# them back or those images get overwritten.
SLOTS=(
  "hero.jpg|plumber-pipes|2000"
  "service-maintenance.jpg|water-heater|1600"
  "gallery-1.jpg|modern-bathroom|1600"
  "gallery-2.jpg|water-heater|1600"
  "gallery-3.jpg|copper-pipes|1600"
  "gallery-4.jpg|kitchen-faucet|1600"
  "gallery-5.jpg|drain-plumbing|1600"
  "gallery-6.jpg|kitchen-sink|1600"
)

USED=""
FAILED=""

for entry in "${SLOTS[@]}"; do
  IFS="|" read -r FILE TERM WIDTH <<< "$entry"
  echo "--> $FILE  (searching Unsplash for '$TERM')"

  # Pull real photo IDs out of the search page HTML
  IDS=$(curl -sL --max-time 40 \
          -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
          "https://unsplash.com/s/photos/${TERM}" \
        | grep -oE 'images\.unsplash\.com/photo-[0-9a-f]{13}-[0-9a-f]{12}' \
        | sed 's#images\.unsplash\.com/##' \
        | sort -u)

  if [ -z "$IDS" ]; then
    echo "    no photo IDs found for '$TERM' — keeping placeholder"
    FAILED="$FAILED $FILE"
    continue
  fi

  GOT=""
  for ID in $IDS; do
    case "$USED" in *"$ID"*) continue ;; esac

    URL="https://images.unsplash.com/${ID}?auto=format&fit=crop&w=${WIDTH}&q=80"
    TMP="$(mktemp)"
    curl -sL --max-time 60 -o "$TMP" "$URL" || { rm -f "$TMP"; continue; }

    # Must be a real JPEG and bigger than 30KB
    if file -b "$TMP" | grep -qi "JPEG image data"; then
      BYTES=$(wc -c < "$TMP")
      if [ "$BYTES" -gt 30720 ]; then
        [ -f "images/$FILE" ] && cp "images/$FILE" "$BACKUP/$FILE" 2>/dev/null
        mv "$TMP" "images/$FILE"
        echo "    ok  $(( BYTES / 1024 ))KB  <- $ID"
        USED="$USED $ID"
        GOT="yes"
        break
      fi
    fi
    rm -f "$TMP"
  done

  if [ -z "$GOT" ]; then
    echo "    every candidate failed verification — keeping placeholder"
    FAILED="$FAILED $FILE"
  fi
done

echo
echo "Verifying images/ ..."
for entry in "${SLOTS[@]}"; do
  IFS="|" read -r FILE _ _ <<< "$entry"
  if [ -f "images/$FILE" ]; then
    printf '  %-24s %s\n' "$FILE" "$(file -b "images/$FILE" | cut -c1-40)"
  else
    printf '  %-24s MISSING\n' "$FILE"
  fi
done

if [ -n "$FAILED" ]; then
  echo
  echo "Still on placeholders:$FAILED"
  echo "Re-run, or drop a photo in by hand using the same filename."
fi

echo
echo "Originals saved in $BACKUP/ — delete that folder once you are happy."
echo "Then update the source column in IMAGES-NEEDED.md and commit."
