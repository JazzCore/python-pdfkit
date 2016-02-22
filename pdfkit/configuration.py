# -*- coding: utf-8 -*-
import sys
from errand_boy.transports.unixsocket import UNIXSocketTransport

errand_boy_transport = UNIXSocketTransport()


class Configuration(object):
    def __init__(self, wkhtmltopdf='', meta_tag_prefix='pdfkit-'):
        self.meta_tag_prefix = meta_tag_prefix

        self.wkhtmltopdf = wkhtmltopdf

        if not self.wkhtmltopdf:
            with errand_boy_transport.get_session() as session:
                subprocess = session.subprocess
                if sys.platform == 'win32':
                    stdout, _ = subprocess.Popen(
                        ['where', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()
                    self.wkhtmltopdf = stdout.strip()
                else:
                    stdout, _ = subprocess.Popen(
                        ['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()
                    self.wkhtmltopdf = stdout.strip()

        try:
            with open(self.wkhtmltopdf) as f:
                pass
        except IOError:
            raise IOError('No wkhtmltopdf executable found: "%s"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install wkhtmltopdf - '
                          'https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf' % self.wkhtmltopdf)
