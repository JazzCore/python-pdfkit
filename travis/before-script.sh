#!/bin/sh

sudo aptitude install -y openssl build-essential xorg libssl-dev
wget http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.11.0_rc1-static-i386.tar.bz2
tar xvjf wkhtmltopdf-0.11.0_rc1-static-i386.tar.bz2
chown root:root wkhtmltopdf-i386
mv wkhtmltopdf-i386 /usr/bin/wkhtmltopdf
