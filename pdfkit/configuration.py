# -*- coding: utf-8 -*-
import subprocess
import sys


class Configuration(object):
    def __init__(self):
        self.meta_tag_prefix = 'pdfkit-'

        self.wkhtmltopdf = ''

        if not self.wkhtmltopdf:
            if sys.platform == 'win32':
                self.wkhtmltopdf = subprocess.Popen(
                    ['where', 'wkhtmltopdf'], shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltopdf = subprocess.Popen(
                    ['which', 'wkhtmltopdf'], shell=True, stdout=subprocess.PIPE).communicate()[0].strip()

        try:
            with open(self.wkhtmltopdf) as f:
                pass
        except IOError:
            raise IOError('No wkhtmltopdf executable found: %s' % self.wkhtmltopdf)
