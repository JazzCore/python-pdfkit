# -*- coding: utf-8 -*-
import re
import subprocess
import sys
from .source import Source
from .configuration import Configuration
from itertools import chain
import io
import codecs


class PDFKit(object):
    """
    url_or_file: str - either a URL, a path to a file or a string containing HTML
                       to convert
    type_:       str - either 'url', 'file' or 'string'
    options:     dict (optional) with wkhtmltopdf options, with or w/o '--'
    toc:         dict (optional) - toc-specific wkhtmltopdf options, with or w/o '--'
    cover:       str (optional) - url/filename with a cover html page
    css:         str (optional) - path to css file which will be added to input string
    configuration: (optional) instance of pdfkit.configuration.Configuration()
    """

    class ImproperSourceError(Exception):
        """Wrong source type for stylesheets"""

        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return self.msg

    def __init__(self, url_or_file, type_, options=None, toc=None, cover=None,
                 css=None, configuration=None):

        self.source = Source(url_or_file, type_)
        self.configuration = Configuration() if configuration is None \
            else configuration

        self.wkhtmltopdf = self.configuration.wkhtmltopdf.decode('utf-8')

        self.options = dict()
        if self.source.isString():
            self.options.update(self._find_options_in_meta(url_or_file))
        if options is not None: self.options.update(options)
        self.options = self._normalize_options(self.options)

        toc = {} if toc is None else toc
        self.toc = self._normalize_options(toc)
        self.cover = cover
        self.css = css
        self.stylesheets = []

    def command(self, path=None):
        if self.css:
            self._prepend_css(self.css)

        args = [self.wkhtmltopdf]

        args += list(chain.from_iterable(list(self.options.items())))
        args = [_f for _f in args if _f]

        if self.toc:
            args.append('toc')
            args += list(chain.from_iterable(list(self.toc.items())))
        if self.cover:
            args.append('cover')
            args.append(self.cover)

        if self.source.isString():
            args.append('-')
        else:
            if isinstance(self.source.source, str):
                args.append(self.source.to_s())
            else:
                args += self.source.source

        if path:
            args.append(path)
        else:
            args.append('-')

        #args = map(lambda x: '"%s"' % x, args)

        return args

    def to_pdf(self, path=None):
        args = self.command(path)

        result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if self.source.isString():
            result.communicate(input=self.source.to_s().encode('utf-8'))
        elif self.source.isFile() and self.css:
            result.communicate(input=self.source.to_s().encode('utf-8'))

        # capture output of wkhtmltopdf and pass it to stdout (can be
        # seen only when running from console )
        if '--quiet' not in args:
            while True:
                if result.poll() is not None:
                    break
                out = result.stdout.read(1).decode('utf-8')
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()

        if path:
            try:
                with codecs.open(path, encoding='utf-8') as f:
                    # read 4 bytes to get PDF signature '%PDF'
                    text = f.read(4)
                    if text == '':
                        raise IOError('Command failed: %s\n'
                                      'Check whhtmltopdf output without \'quiet\' '
                                      'option' % ' '.join(args))
                    return text
            except IOError:
                raise IOError('Command failed: %s\n'
                              'Check whhtmltopdf output without \'quiet\' option' %
                              ' '.join(args))

    def to_file(self, path):
        self.to_pdf(path)

    def _normalize_options(self, options):
        normalized_options = {}

        for key, value in list(options.items()):
            if not '--' in key:
                normalized_key = '--%s' % self._normalize_arg(key)
            else:
                normalized_key = self._normalize_arg(key)
            normalized_options[normalized_key] = str(value) if value else value

        return normalized_options

    def _normalize_arg(self, arg):
        return arg.lower()

    def _style_tag_for(self, stylesheet):
        return "<style>%s</style>" % stylesheet

    def _prepend_css(self, path):
        if self.source.isUrl() or isinstance(self.source.source, list):
            raise self.ImproperSourceError('CSS file can be added only to a single '
                                           'file or string')

        with open(path) as f:
            css_data = f.read()

        if self.source.isFile():
            with open(self.source.to_s()) as f:
                inp = f.read()
            self.source = Source(
                inp.replace('</head>', self._style_tag_for(css_data) + '</head>'),
                'string')

        elif self.source.isString():
            if '</head>' in self.source.to_s():
                self.source.source = self.source.to_s().replace(
                    '</head>', self._style_tag_for(css_data) + '</head>')
            else:
                self.source.source = self._style_tag_for(css_data) + self.source.to_s()

    def _find_options_in_meta(self, content):
        if isinstance(content, io.IOBase) \
                or content.__class__.__name__ == 'StreamReaderWriter':
            content = content.read()

        found = {}

        for x in re.findall('<meta [^>]*>', content):
            if re.search('name=["\']%s' % self.configuration.meta_tag_prefix, x):
                name = re.findall('name=["\']%s([^"\']*)' %
                                  self.configuration.meta_tag_prefix, x)[0]
                found[name] = re.findall('content=["\']([^"\']*)', x)[0]

        return found
