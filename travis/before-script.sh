#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.6-1'

sudo apt-get install -y openssl build-essential libssl-dev libxrender1 libfontconfig1 libx11-dev fontconfig xfonts-75dpi xfonts-base
wget "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb"
sudo dpkg -i wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb
sudo apt-get -f install