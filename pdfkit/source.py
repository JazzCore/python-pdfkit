# -*- coding: utf-8 -*-


class Source(object):
    def __init__(self, url_or_file, type_):
        self.source = url_or_file
        self.type = type_

    def isUrl(self):
        return 'url' in self.type

    def isFile(self, path=None):
        #dirty hack to check where file is opened with codecs module ( because it returns 'instance' type when encoding
        #is specified
        if path:
            return isinstance(path, file) or path.__class__.__name__ == 'StreamReaderWriter'
        else:
            return 'file' in self.type

#    def isHtml(self):
#        return not (self.isUrl() or self.isFile())
    def isString(self):
        return 'string' in self.type

    def to_s(self):
        return self.source
