#!/bin/sh
# Monta a pasta dist/ só com os arquivos públicos do site (docs/ fica de fora).
# Cloudflare Pages: build command "sh build.sh", output directory "dist".
set -e
rm -rf dist
mkdir dist
cp -r index.html 404.html styles.css script.js assets favicon.ico \
  site.webmanifest robots.txt sitemap.xml _headers waba dist/
