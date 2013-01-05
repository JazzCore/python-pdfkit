# -*- coding: utf-8 -*-
import os

import unittest

import pdfkit

class TestPDFKit(unittest.TestCase):
    def setUp(self):
        pass

    def test_html_source_line(self):
        r = pdfkit.PDFKit('<h1>Oh hai</h1>', 'string')
        self.assertTrue(r.source.isString())

    def test_url(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url')
        self.assertTrue(r.source.isUrl())

    def test_options_parsing(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter'})
        self.assertTrue(r.options['--page-size'])

    def test_command(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter', 'toc-l1-font-size': 12})
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
        r = pdfkit.PDFKit('html', 'string')
        self.assertEqual(r.command()[-2:], ['-', '-'])

    def test_url_to_the_source(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url')
        self.assertEqual(r.command()[-2:], ['http://ya.ru', '-'])

    def test_path_to_the_file(self):
        path = 'testfiles/example.html'
        r = pdfkit.PDFKit(path, 'file')
        self.assertEqual(r.command()[-2:], [path, '-'])

    def test_output_path(self):
        out = '/test/test2/out.pdf'
        r = pdfkit.PDFKit('html', 'string')
        self.assertEqual(r.command(out)[-1:], ['/test/test2/out.pdf'])

    def test_pdfkit_meta_tags(self):
        body = """
        <html>
          <head>
            <meta name="pdfkit-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
        """

        r = pdfkit.PDFKit(body, 'string')
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

        r = pdfkit.PDFKit(body, 'string')
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

        r = pdfkit.PDFKit(body, 'string')
        command = r.command()
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_pdf_generation(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter'})
        pdf = r.to_pdf('ouy.pdf')
        self.assertEqual(pdf[:4], '%PDF')
        os.remove('ouy.pdf')

    def test_toc_handling_without_options(self):
        r = pdfkit.PDFKit('hmtl', 'string', toc={'xsl-style-sheet': 'test.xsl'})
        self.assertEqual(r.command()[1], 'toc')
        self.assertEqual(r.command()[2], '--xsl-style-sheet')

    def test_toc_with_options(self):
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = pdfkit.PDFKit('html', 'string', options=options, toc={'xsl-style-sheet': 'test.xsl'})

        self.assertEqual(r.command()[1 + len(options) * 2], 'toc')
        self.assertEqual(r.command()[1 + len(options) * 2 + 1], '--xsl-style-sheet')

    def test_cover_without_options(self):
        r = pdfkit.PDFKit('html', 'string', cover='test.html')

        self.assertEqual(r.command()[1], 'cover')
        self.assertEqual(r.command()[2], 'test.html')

    def test_cover_with_options(self):
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = pdfkit.PDFKit('html', 'string', options=options, cover='test.html')

        self.assertEqual(r.command()[1 + len(options) * 2], 'cover')
        self.assertEqual(r.command()[1 + len(options) * 2 + 1], 'test.html')

    def test_cover_and_toc(self):
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = pdfkit.PDFKit('html', 'string', options=options, toc={'xsl-style-sheet': 'test.xsl'}, cover='test.html')
        command = r.command()
        self.assertEqual(command[-7:], ['toc', '--xsl-style-sheet', 'test.xsl', 'cover', 'test.html', '-', '-'])

    def test_stylesheet_adding_to_the_head(self):
        #TODO rewrite this part of pdfkit.py
        r = pdfkit.PDFKit('<html><head></head><body>Hai!</body></html>', 'string')
        css = open('testfiles/example.css')
        r.stylesheets.append(css)
        r.to_pdf()
        self.assertIn('<style>%s</style><html>' % css.read(), r.source.to_s())

    def test_stylesheet_adding_without_head_tag(self):
        #TODO rewrite this part of pdfkit.py
        r = pdfkit.PDFKit('<html><body>Hai!</body></html>', 'string')
        css = open('testfiles/example.css')
        r.stylesheets.append(css)
        r.to_pdf()
        self.assertIn('<style>%s</style><html>' % css.read(), r.source.to_s())

    def test_stylesheet_throw_error_when_url(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url')
        css = open('testfiles/example.css')
        r.stylesheets.append(css)
        with self.assertRaises(r.ImproperSourceError):
            r.to_pdf()

    def test_stylesheet_adding_to_file_with_option(self):
        css = 'testfiles/example.css'
        r = pdfkit.PDFKit('testfiles/example.html', 'file', css=css)
        self.assertEqual(r.css, css)
        self.assertIn('font-size', r._prepend_css(css))

    def test_raise_error_with_wrong_css_path(self):
        css = 'testfiles/wrongpath.css'
        r = pdfkit.PDFKit('testfiles/example.html', 'file', css=css)
        with self.assertRaises(IOError):
            r.to_pdf()

    def test_raise_error_if_css_added_to_url_or_string(self):
        css = 'testfiles/example.css'
        r = pdfkit.PDFKit('test', 'string', css=css)
        r2 = pdfkit.PDFKit('http://google.com', 'url', css=css)
        with self.assertRaises(r.ImproperSourceError):
            r._prepend_css(css)
        with self.assertRaises(r.ImproperSourceError):
            r2._prepend_css(css)

    def test_lists_of_input_args(self):
        urls = ['http://ya.ru', 'http://google.com']
        paths = ['testfiles/example.html', 'testfiles/examples.html']
        r = pdfkit.PDFKit(urls, 'url')
        r2 = pdfkit.PDFKit(paths, 'file')
        cmd = r.command()
        cmd2 = r2.command()
        self.assertEqual(cmd[-3:], ['http://ya.ru', 'http://google.com', '-'])
        self.assertEqual(cmd2[-3:], ['testfiles/example.html', 'testfiles/examples.html', '-'])

if __name__ == "__main__":
    unittest.main()
