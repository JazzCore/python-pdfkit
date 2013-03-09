#!/bin/sh

sudo apt-get install -y openssl build-essential xorg libssl-dev
wget http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.10.0_rc2-static-amd64.tar.bz2
tar xvjf wkhtmltopdf-0.10.0_rc2-static-amd64.tar.bz2
sudo chown root:root wkhtmltopdf-amd64
sudo mv wkhtmltopdf-amd64 /usr/bin/wkhtmltopdf
