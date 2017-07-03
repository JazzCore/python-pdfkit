#!/bin/sh

sudo apt-get install -y openssl build-essential xorg libssl-dev
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
cd wkhtmltox
sudo chown root:root bin/wkhtmltopdf
sudo cp -r * /usr/
