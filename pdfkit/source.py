# -*- coding: utf-8 -*-


class Source(object):
    def __init__(self, url_or_file):
        self.source = url_or_file

    def isUrl(self):
        return type(self.source) is str and 'http' in self.source

    def isFile(self):
        #dirty hack to check where file is opened with codecs module ( because it returns 'instance' type when encoding
        #is specified
        return type(self.source) is file or self.source.__class__.__name__ == 'StreamReaderWriter'

    def isHtml(self):
        return not (self.isUrl() or self.isFile())

    def to_s(self):
        return self.source.name if self.isFile() else self.source

    pass


