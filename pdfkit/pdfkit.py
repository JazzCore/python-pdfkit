# -*- coding: utf-8 -*-
import re
import subprocess
import sys
from source import Source
from configuration import Configuration
from itertools import chain


class PDFKit(object):
    class NoExecutableError(Exception):
        """Wkhtmltopdf executable not found"""

        def __str__(self):
            #TODO insert actual path
            return ("No wkhtmltopdf executable found.\n"
                    "Please install wkhtmltopdf - https://github.com/jdpace/PDFKit/wiki/Installing-WKHTMLTOPDF")

    class ImproperSourceError(Exception):
        """Wrong source type for stylesheets"""

        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return self.msg

    def __init__(self, url_or_file, type_, options=None, toc=None, cover=None, css=None):
        options = {} if options is None else options
        toc = {} if toc is None else toc
        #TODO rework wkhtml path set and check
        #TODO outline tests
        self.source = Source(url_or_file, type_)
        self.configuration = Configuration()
        self.options = dict()
        self.stylesheets = []

        self.wkhtmltopdf = self.configuration.wkhtmltopdf

        if self.source.isString():
            self.options.update(self._find_options_in_meta(url_or_file))

        self.options.update(options)
        self.options = self._normalize_options(self.options)
        self.toc = self._normalize_options(toc)
        self.cover = cover
        self.css = css

        try:
            with open(self.wkhtmltopdf) as f:
                pass
        except IOError:
            raise self.NoExecutableError()

    def command(self, path=None):
        args = [self.wkhtmltopdf]

        args += list(chain.from_iterable(self.options.items()))
        args = filter(self._isTrue, args)

        if self.toc:
            args.append('toc')
            args += list(chain.from_iterable(self.toc.items()))
        if self.cover:
            args.append('cover')
            args.append(self.cover)

#args.append('--quiet')

        if self.source.isString() or self.css:
            args.append('-')
        else:
            if isinstance(self.source, str):
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
        self._append_stylesheets()

        args = self.command(path)
        #invoke = ' '.join(args)

        result = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if self.css:
            data = self._prepend_css(self.css)
            result.communicate(input=data.encode('utf-8'))
        elif self.source.isString():
            result.communicate(input=self.source.to_s().encode('utf-8'))
            #TODO wip

        #capture output of wkhtmltopdf and pass it to stdout ( can be seen only when running from console )
        if '--quiet' not in args:
            while True:
                out = result.stdout.read(1)
                if out == '' and result.poll() is not None:
                    break
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()

        if path:
            text = open(path).read()

            if text == '':
                raise 'command failed: %s' % ' '.join(args)
            return text

    def to_file(self, path):
        self.to_pdf(path)

    def _normalize_options(self, options):
        normalized_options = {}

        for key, value in options.iteritems():
            normalized_key = '--%s' % self._normalize_arg(key)
            normalized_options[normalized_key] = self._normalize_value(value)

        return normalized_options

    def _normalize_arg(self, arg):
        return arg.lower()

    def _normalize_value(self, value):
        if isinstance(value, bool):
            return None
        else:
            return str(value)
            #TODO Guess this is not needed - Popen automatically quotes args
            #            value = str(value)
            #            if value.split(' ') == [value]:
            #                return value
            #            else:
            #                return '"%s"' % value

    def _style_tag_for(self, stylesheet):
        if self.source.isFile(stylesheet):
            return "<style>%s</style>" % stylesheet.read()
        else:
            return "<style>%s</style>" % stylesheet

    def _prepend_css(self, path):
        if not self.source.isFile():
                raise self.ImproperSourceError('CSS file can be prepended only to a file or to an raw HTML source')

        with open(path) as f:
            data = f.read()

        with open(self.source.to_s()) as f:
            out = f.read()

        ret = out.replace('</head>', self._style_tag_for(data) + '</head>')
        return ret

    def _append_stylesheets(self):
        if self.stylesheets and not self.source.isString():
            raise self.ImproperSourceError('Stylesheets may only be added to an HTML source')

        for x in self.stylesheets:
            if '</head>' in x:
                self.source = Source(self.source.to_s.replace('</head>', self._style_tag_for(x) + '</head>'))
            else:
                self.source.source = self._style_tag_for(x) + self.source.source

    def _isTrue(self, x):
        if x is None:
            return 0
        else:
            return 1

    def _find_options_in_meta(self, content):
        if isinstance(content, file) or content.__class__.__name__ == 'StreamReaderWriter':
            content = content.read()

        found = {}

        for x in re.findall('<meta [^>]*>', content):
            if re.search('name=["\']%s' % self.configuration.meta_tag_prefix, x):
                name = re.findall('name=["\']%s([^"\']*)' % self.configuration.meta_tag_prefix, x)[0]
                found[name] = re.findall('content=["\']([^"\']*)', x)[0]

        return found