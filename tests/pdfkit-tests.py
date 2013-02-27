# -*- coding: utf-8 -*-
import os
import io
import sys
import codecs
import unittest

#Prepend ../ to PYTHONPATH so that we can import PDFKIT form there.
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, '..')))

import pdfkit


class TestPDFKitInitialization(unittest.TestCase):
    """Test init"""

    def test_html_source(self):
        r = pdfkit.PDFKit('<h1>Oh hai</h1>', 'string')
        self.assertTrue(r.source.isString())

    def test_url_source(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url')
        self.assertTrue(r.source.isUrl())

    def test_file_source(self):
        r = pdfkit.PDFKit('fixtures/example.html', 'file')
        self.assertTrue(r.source.isFile())

    def test_file_source_with_path(self):
        r = pdfkit.PDFKit('test', 'string')
        with io.open('fixtures/example.css') as f:
            self.assertTrue(r.source.isFile(path=f))
        with codecs.open('fixtures/example.css', encoding='UTF-8') as f:
            self.assertTrue(r.source.isFile(path=f))

    def test_options_parsing(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter'})
        self.assertTrue(r.options['--page-size'])

    def test_options_parsing_with_dashes(self):
        r = pdfkit.PDFKit('html', 'string', options={'--page-size': 'Letter'})
        self.assertTrue(r.options['--page-size'])


class TestPDFKitCommandGeneration(unittest.TestCase):
    """Test command() method"""

    def test_command_construction(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter', 'toc-l1-font-size': 12})
        command = r.command()
        self.assertEqual(command[0], r.wkhtmltopdf)
        self.assertEqual(command[command.index('--page-size') + 1], 'Letter')
        self.assertEqual(command[command.index('--toc-l1-font-size') + 1], '12')

    def test_lists_of_input_args(self):
        urls = ['http://ya.ru', 'http://google.com']
        paths = ['fixtures/example.html', 'fixtures/example.html']
        r = pdfkit.PDFKit(urls, 'url')
        r2 = pdfkit.PDFKit(paths, 'file')
        cmd = r.command()
        cmd2 = r2.command()
        self.assertEqual(cmd[-3:], ['http://ya.ru', 'http://google.com', '-'])
        self.assertEqual(cmd2[-3:], ['fixtures/example.html', 'fixtures/example.html', '-'])

    def test_read_source_from_stdin(self):
        r = pdfkit.PDFKit('html', 'string')
        self.assertEqual(r.command()[-2:], ['-', '-'])

    def test_url_in_command(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url')
        self.assertEqual(r.command()[-2:], ['http://ya.ru', '-'])

    def test_file_path_in_command(self):
        path = 'fixtures/example.html'
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

    def test_outline_options(self):
        options = {
            'outline': None,
            'outline-depth': 1
        }

        r = pdfkit.PDFKit('ya.ru', 'url', options=options)
        cmd = r.command()
        #self.assertEqual(cmd[1:], ['--outline', '--outline-depth', '1', 'ya.ru', '-'])
        self.assertIn('--outline', cmd)
        self.assertEqual(cmd[cmd.index('--outline-depth') + 1], '1')

    def test_filter_empty_and_none_values_in_opts(self):
        options = {
            'outline': '',
            'footer-line': None,
            'quiet': False
        }

        r = pdfkit.PDFKit('html', 'string', options=options)
        cmd = r.command()
        self.assertEqual(len(cmd), 6)


class TestPDFKitGeneration(unittest.TestCase):
    """Test to_pdf() method"""

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists('out.pdf'):
            os.remove('out.pdf')

    def test_pdf_generation(self):
        r = pdfkit.PDFKit('html', 'string', options={'page-size': 'Letter'})
        pdf = r.to_pdf('out.pdf')
        self.assertEqual(pdf[:4], '%PDF')

    def test_raise_error_with_invalid_url(self):
        r = pdfkit.PDFKit('wrongurl', 'url')
        with self.assertRaises(IOError):
            r.to_pdf('out.pdf')

    def test_raise_error_with_invalid_file_path(self):
        paths = ['frongpath.html', 'wrongpath2.html']
        with self.assertRaises(IOError):
            pdfkit.PDFKit('wrongpath.html', 'file')
        with self.assertRaises(IOError):
            pdfkit.PDFKit(paths, 'file')

    def test_stylesheet_adding_to_the_head(self):
        #TODO rewrite this part of pdfkit.py
        r = pdfkit.PDFKit('<html><head></head><body>Hai!</body></html>', 'string',
                          css='fixtures/example.css')

        with open('fixtures/example.css') as f:
            css = f.read()

        r._prepend_css('fixtures/example.css')
        self.assertIn('<style>%s</style>' % css, r.source.to_s())

    def test_stylesheet_adding_without_head_tag(self):
        r = pdfkit.PDFKit('<html><body>Hai!</body></html>', 'string',
                          options={'quiet': None}, css='fixtures/example.css')

        with open('fixtures/example.css') as f:
            css = f.read()

        r._prepend_css('fixtures/example.css')
        self.assertIn('<style>%s</style><html>' % css, r.source.to_s())

    def test_stylesheet_throw_error_when_url(self):
        r = pdfkit.PDFKit('http://ya.ru', 'url', css='fixtures/example.css')

        with self.assertRaises(r.ImproperSourceError):
            r.to_pdf()

    def test_stylesheet_adding_to_file_with_option(self):
        css = 'fixtures/example.css'
        r = pdfkit.PDFKit('fixtures/example.html', 'file', css=css)
        self.assertEqual(r.css, css)
        r._prepend_css(css)
        self.assertIn('font-size', r.source.to_s())

    def test_pdf_generation_from_file_like(self):
        with open('fixtures/example.html', 'r') as f:
            r = pdfkit.PDFKit(f, 'file')
            output = r.to_pdf()
        self.assertEqual(output[:4], '%PDF')

    def test_raise_error_with_wrong_css_path(self):
        css = 'fixtures/wrongpath.css'
        r = pdfkit.PDFKit('fixtures/example.html', 'file', css=css)
        with self.assertRaises(IOError):
            r.to_pdf()

if __name__ == "__main__":
    unittest.main()
