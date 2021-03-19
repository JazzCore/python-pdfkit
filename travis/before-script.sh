#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.6-1'

sudo apt-get install -y openssl build-essential xorg libssl-dev libxrender1 libfontconfig1 libx11-dev libjpeg62 libxtst6 fontconfig xfonts-75dpi xfonts-base libpng12-0
https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
wget "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}.focal_amd64.deb"
sudo dpkg -i wkhtmltox_${WKHTML2PDF_VERSION}.focal_amd64.deb
sudo apt-get -f install