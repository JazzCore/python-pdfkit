Python-PDFKit: HTML to PDF wrapper
==================================

Python wrapper for wkhtmltopdf utility to convert HTML to PDF using Webkit.

This is adapted version of `ruby PDFKit <https://github.com/pdfkit/pdfkit>`_ library, so big thanks to them!

Installation
------------

1. Install python-pdfkit:

.. code-block:: bash

	$ pip install pdfkit

2. Install wkhtmltopdf:

* Debian/Ubuntu:

.. code-block:: bash

	$ sudo apt-get install wkhtmltopdf

**Warning!** Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from `wkhtmltopdf <http://code.google.com/p/wkhtmltopdf/>`_ site or you can use `this script <https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh>`_.

* Windows and other options: check wkhtmltopdf `homepage <http://code.google.com/p/wkhtmltopdf/>`_ for binary installers

Usage
-----

For simple tasks:

.. code-block:: python

	import pdfkit

	pdfkit.from_url('http://google.com', 'out.pdf')
	pdfkit.from_file('test.html', 'out.pdf')
	pdfkit.from_string('Hello!', 'out.pdf')

You can pass a list with multiple URLs or files:

.. code-block:: python

	pdfkit.from_url(['google.com', 'yandex.ru', 'engadget.com'], 'out.pdf')
	pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')

You can specify all wkhtmltopdf `options <http://madalgo.au.dk/~jakobt/wkhtmltoxdoc/wkhtmltopdf_0.10.0_rc2-doc.html>`_. You can drop '--' in option name. If option without value, use *None, False* or *''* for dict value:

.. code-block:: python

	options = {
	    'page-size': 'Letter',
	    'margin-top': '0.75in',
	    'margin-right': '0.75in',
	    'margin-bottom': '0.75in',
	    'margin-left': '0.75in',
	    'encoding': "UTF-8",
	    'no-outline': None
	}

	pdfkit.from_url('http://google.com', 'out.pdf', options=options)


Due to wkhtmltopdf command syntax, **TOC** and **Cover** options must be specified separately:

.. code-block:: python

	toc = {
	    'xsl-style-sheet': 'toc.xsl'
	}

	cover = 'cover.html'

	pdfkit.from_file('file.html', options=options, toc=toc, cover=cover)

You can specify external CSS file when converting files or strings using *css* option.

**Warning** This is a workaround for `this bug <http://code.google.com/p/wkhtmltopdf/issues/detail?id=144>`_ in wkhtmltopdf. You should try *--user-style-sheet* option first.

.. code-block:: python

	css = 'example.css'

	pdfkit.from_file('file.html', options=options, css=css)

You can also pass any options through meta tags in your HTML:

.. code-block:: python

	body = """
	    <html>
	      <head>
	        <meta name="pdfkit-page-size" content="Legal"/>
	        <meta name="pdfkit-orientation" content="Landscape"/>
	      </head>
	      Hello World!
	      </html>
	    """

	pdfkit.from_string(body, 'out.pdf') #with --page-size=Legal and --orientation=Landscape

Troubleshooting
---------------

- ``IOError: 'No wkhtmltopdf executable found'``:

  Make sure that you have wkhtmltopdf in your PATH. *where wkhtmltopdf* in Windows or *which wkhtmltopdf* on Linux should return actual path to binary.
