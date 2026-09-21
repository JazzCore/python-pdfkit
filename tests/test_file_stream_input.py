import io
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import pdfkit


class FileStreamInputTests(unittest.TestCase):
    def convert(self, stream, expected):
        config = pdfkit.configuration(wkhtmltopdf=sys.executable)
        process = Mock(returncode=0)
        process.communicate.return_value = (b'%PDF-test-output', b'')
        with patch('pdfkit.pdfkit.subprocess.Popen', return_value=process):
            output = pdfkit.from_file(stream, configuration=config)
        self.assertEqual(output, b'%PDF-test-output')
        process.communicate.assert_called_once_with(input=expected)
        self.assertFalse(stream.closed)

    def test_binary_memory_stream(self):
        data = '<p>café</p>'.encode('utf-8')
        self.convert(io.BytesIO(data), data)

    def test_binary_file_preserves_declared_encoding(self):
        data = b'<meta charset="iso-8859-1"><p>caf\xe9</p>'
        with tempfile.TemporaryFile('w+b') as stream:
            stream.write(data)
            stream.seek(0)
            self.convert(stream, data)

    def test_text_stream_is_encoded_as_utf8(self):
        self.convert(io.StringIO('<p>café</p>'), '<p>café</p>'.encode('utf-8'))

    def test_empty_binary_stream(self):
        self.convert(io.BytesIO(b''), b'')
