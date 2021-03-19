#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.6-1'

sudo apt-get install -y build-essential xorg libssl-dev libxrender-dev wget gdebi
wget "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb"
sudo gdebi --n wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb
