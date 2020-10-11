#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

GOOGLE_USERNAME="julius.dehner@gmail.com"
GOOGLE_PASSWORD=$(gopass show -o Account/google.com/${GOOGLE_USERNAME})

python src/g2a_auctio/main.py $GOOGLE_USERNAME $GOOGLE_PASSWORD
