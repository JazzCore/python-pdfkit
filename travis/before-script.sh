#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.6-1'

sudo apt-get install -y openssl build-essential libssl-dev libpthread-stubs0-dev libxau-dev xorg-sgml-doctools libxdmcp-dev x11proto-core-dev x11proto-input-dev x11proto-kb-dev xtrans-dev libx11-dev libxcb1-dev libjpeg62 libxtst6 libfontenc1 libxfont1 x11-common xfonts-encodings xfonts-utils fontconfig xfonts-base xfonts-75dpi
wget "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}.xenial_amd64.deb"
sudo dpkg -i wkhtmltox_${WKHTML2PDF_VERSION}.xenial_amd64.deb
sudo apt-get -f install