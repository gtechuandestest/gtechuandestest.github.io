#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Descarga las fotos oficiales de los cinco directores desde el portal de
# investigadores UANDES, las deja cuadradas (640×640) en assets/img/people/ y
# enlaza cada una en _data/people.yml (campo `photo`).
#
# Se corre desde el Mac, en la raíz del repo:
#     bash herramientas/fotos-directores.sh
#
# Es idempotente: si la foto ya existe no la vuelve a bajar; si el campo
# `photo` ya está lleno no lo toca. Para forzar la descarga: FORZAR=1 bash ...
#
# Las URLs salen de informacion/perfiles/*/*.md (campo `foto:`). Si UANDES
# cambia una, se actualiza acá.
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")/.."

DEST="assets/img/people"
LADO=640
mkdir -p "$DEST"

# id en people.yml | archivo destino | URL
FOTOS="
cesar-huilinir|cesar-huilinir.jpg|https://investigadores.uandes.cl/files-asset/72339018/Cesar_Huili_ir.jpg
alberto-vergara|alberto-vergara.jpg|https://investigadores.uandes.cl/files-asset/34208820/AVergara.jpg
felipe-scott|felipe-scott.jpg|https://investigadores.uandes.cl/files-asset/85825495/Felipe_Scott.jpg
sichem-guerrero|sichem-guerrero.jpg|https://investigadores.uandes.cl/files-asset/34208756/SichemGuerrero.jpg.jpg
patricio-moreno|patricio-moreno.jpg|https://investigadores.uandes.cl/files-asset/34208850/PatricioMoreno.jpg.jpg
"

cuadrar() {   # cuadrar <archivo>  → recorta al centro y deja LADO×LADO
  local f="$1"
  if command -v magick >/dev/null 2>&1; then
    magick "$f" -auto-orient -gravity center -resize "${LADO}x${LADO}^" -extent "${LADO}x${LADO}" -quality 88 "$f"
  elif command -v sips >/dev/null 2>&1; then
    local w h
    w=$(sips -g pixelWidth  "$f" | awk '/pixelWidth/  {print $2}')
    h=$(sips -g pixelHeight "$f" | awk '/pixelHeight/ {print $2}')
    if [ "$w" -lt "$h" ]; then sips --resampleWidth  "$LADO" "$f" >/dev/null
    else                       sips --resampleHeight "$LADO" "$f" >/dev/null; fi
    sips -c "$LADO" "$LADO" "$f" >/dev/null
  else
    echo "   (sin magick ni sips: se deja la foto tal cual)"
  fi
}

enlazar() {   # enlazar <id> <archivo>  → photo: "" → photo: "<archivo>" solo en ese bloque
  local id="$1" file="$2" tmp
  tmp=$(mktemp)
  awk -v id="$id" -v file="$file" '
    /^- id: / { cur = $3 }
    cur == id && /^  photo: ""/ { sub(/""/, "\"" file "\""); hecho = 1 }
    { print }
    END { if (!hecho) print "   (photo ya estaba enlazada o no se encontró el bloque " id ")" > "/dev/stderr" }
  ' _data/people.yml > "$tmp" && mv "$tmp" _data/people.yml
}

echo "$FOTOS" | while IFS='|' read -r id file url; do
  [ -z "$id" ] && continue
  out="$DEST/$file"
  if [ -s "$out" ] && [ "${FORZAR:-0}" != "1" ]; then
    echo "✓ $file ya existe"
  else
    echo "↓ $file"
    curl -fsSL --retry 2 -o "$out" "$url" || { echo "   ✗ no se pudo bajar $url"; rm -f "$out"; continue; }
    cuadrar "$out"
  fi
  enlazar "$id" "$file"
done

echo
echo "Listo. Revisa con: bundle exec jekyll serve   (y git diff _data/people.yml)"
