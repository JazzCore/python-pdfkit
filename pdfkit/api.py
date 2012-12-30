# -*- coding: utf-8 -*-

from .pdfkit import PDFKit


def from_url(url, output_path, options=None, toc=None, cover=None):
#TODO rework
    """
    Convert file of files from URLs to PDF document

    :param url: URL or list of URLs to be saved
    :param output_path: path to output PDF file
    :param options: (optional) dict with wkhtmltopdf global and page options, without '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, without '--'
    :param cover: (optional) string with url/filename with a cover html page
    """

    r = PDFKit(url, options=options, toc=toc,cover=cover)

    r.to_file(output_path)


def from_file(input, output_path, options=None, toc=None, cover=None):
    """
    Convert HTML file or files to PDF document

    :param input: path to HTML file or list with paths
    :param output_path: path to output PDF file
    :param options: (optional) dict with wkhtmltopdf options, without '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, without '--'
    :param cover: (optional) string with url/filename with a cover html page

    """
    pass


def from_string(input, output_path, options=None, toc=None, cover=None):
    """
    Convert given string or strings to PDF document

    :param input: string or list of strings. Could be a raw text or a html file
    :param output_path: path to output PDF file
    :param options: (optional) dict with wkhtmltopdf options, without '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, without '--'
    :param cover: (optional) string with url/filename with a cover html page

    """

    pass