#!/usr/bin/env bash
# Idempotent install of the PDF/OCR toolchain used by internal/scripts/.
# Safe to re-run. Does not change the personal Cloud Agent snapshot by itself —
# run this on a fresh VM (or bake it into the environment install) so tesseract
# and the Python PDF libs are present before ocr-text-layer.py.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

install_tesseract() {
  if command -v tesseract >/dev/null 2>&1; then
    echo "tesseract already on PATH: $(command -v tesseract)"
    return 0
  fi
  if ! command -v apt-get >/dev/null 2>&1; then
    echo "tesseract not found. Install tesseract-ocr (Debian: apt-get; macOS: brew install tesseract)" >&2
    return 1
  fi
  echo "Installing tesseract-ocr via apt-get…"
  if [ "$(id -u)" -eq 0 ]; then
    apt-get update -qq
    apt-get install -y tesseract-ocr
  elif command -v sudo >/dev/null 2>&1; then
    sudo apt-get update -qq
    sudo apt-get install -y tesseract-ocr
  else
    echo "Need root or sudo to apt-get install tesseract-ocr" >&2
    return 1
  fi
}

install_tesseract
python3 -m pip install -r "$ROOT/requirements.txt"
echo "tesseract: $(tesseract --version 2>/dev/null | head -n 1)"
python3 -c "import reportlab, pypdf, fitz, pytesseract; print('python pdf libs ok')"
