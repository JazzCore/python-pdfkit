#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.6-1'

sudo apt install -y build-essential xorg libssl-dev libxrender-dev wget
wget "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb"
sudo apt install -y ./wkhtmltox_${WKHTML2PDF_VERSION}.bionic_amd64.deb
