# -*- coding: utf-8 -*-
import os

import unittest

import pdfkit

class TestPDFKit(unittest.TestCase):

    def setUp(self):
        pass

    def test_html_source_line(self):
        r = pdfkit.PDFKit('<h1>Oh hai</h1>')
        self.assertTrue(r.source.isHtml())

    def test_url(self):
        r = pdfkit.PDFKit('http://ya.ru')
        self.assertTrue(r.source.isUrl())

    def test_options_parsing(self):
        r = pdfkit.PDFKit('html', options={'page-size' : 'Letter'})
        self.assertTrue(r.options['--page-size'])

    def test_command(self):
        r = pdfkit.PDFKit('html',options={'page-size': 'Letter', 'toc-l1-font-size': 12})
        command = r.command()
        self.assertEqual(command[0], r.wkhtmltopdf)
        self.assertEqual(command[command.index('--page-size') + 1], 'Letter')
        self.assertEqual(command[command.index('--toc-l1-font-size') + 1], '12')

#Not needed, Popen automatically quotes args (?)
#    def test_string_quote_encapsulation(self):
#        r = pdfkit.PDFKit('html', options={'header-center': 'foo [page]'})
#        command = r.command()
#        self.assertEqual(command[command.index('--header-center') + 1], '"foo [page]"')

    def test_read_source_from_stdin(self):
        r = pdfkit.PDFKit('html')
        self.assertEqual(r.command()[-2:], ['-', '-'])

    def test_url_to_the_source(self):
        r = pdfkit.PDFKit('http://ya.ru')
        self.assertEqual(r.command()[-2:], ['http://ya.ru', '-'])

    def test_path_to_the_file(self):
        path = 'pdfkit/pdfkit.py'
        r = pdfkit.PDFKit(open(path))
        self.assertEqual(r.command()[-2:], [path, '-'])

    def test_output_path(self):
        out = '/test/test2/out.pdf'
        r = pdfkit.PDFKit('html')
        self.assertEqual(r.command(out)[-1:], ['/test/test2/out.pdf'])

    def test_pdfkit_meta_tags(self):
        body = """
        <html>
          <head>
            <meta name="pdfkit-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
        </html>
        """

        r = pdfkit.PDFKit(body)
        command = r.command()
        self.assertEqual(command[command.index('--page-size') + 1], 'Legal')
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_pdfkit_meta_tags_in_bad_markup(self):
        body = """
        <html>
          <head>
            <meta name="pdfkit-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
          <br>
        </html>
        """

        r = pdfkit.PDFKit(body)
        command = r.command()
        self.assertEqual(command[command.index('--page-size') + 1], 'Legal')
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_skip_nonpdfkit_tags(self):
        body = """
        <html>
          <head>
            <meta name="test-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
          <br>
        </html>
        """

        r = pdfkit.PDFKit(body)
        command = r.command()
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_pdf_generation(self):
        r = pdfkit.PDFKit('html', options={'page-size': 'Letter'})
        pdf = r.to_pdf('ouy.pdf')
        self.assertEqual(pdf[:4], '%PDF')
        os.remove('ouy.pdf')

if __name__ == "__main__":
    unittest.main()
