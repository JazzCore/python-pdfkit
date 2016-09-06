# -*- coding: utf-8 -*-

from .pdfkit import PDFKit
from .pdfkit import Configuration


def from_url(url, output_path, options=None, cover=None, toc=None, configuration=None):
    """
    Convert file of files from URLs to PDF document

    :param url: URL or list of URLs to be saved
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf global and page options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()

    Returns: True on success
    """

    r = PDFKit(url, 'url', options=options, cover=cover, toc=toc,
               configuration=configuration)

    return r.to_pdf(output_path)


def from_file(input, output_path, options=None, cover=None, toc=None, css=None,
              configuration=None):
    """
    Convert HTML file or files to PDF document

    :param input: path to HTML file or list with paths or file-like object
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param css: (optional) string with path to css file which will be added to a single input file
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()

    Returns: True on success
    """

    r = PDFKit(input, 'file', options=options, cover=cover, toc=toc, css=css,
               configuration=configuration)

    return r.to_pdf(output_path)


def from_string(input, output_path, options=None, cover=None, toc=None, css=None,
                configuration=None):
    """
    Convert given string or strings to PDF document

    :param input: string with a desired text. Could be a raw text or a html file
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param css: (optional) string with path to css file which will be added to a input string
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()

    Returns: True on success
    """

    r = PDFKit(input, 'string', options=options, cover=cover, toc=toc, css=css,
               configuration=configuration)

    return r.to_pdf(output_path)


def configuration(**kwargs):
    """
    Constructs and returns a :class:`Configuration` with given options

    :param wkhtmltopdf: path to binary
    :param meta_tag_prefix: the prefix for ``pdfkit`` specific meta tags
    """

    return Configuration(**kwargs)
