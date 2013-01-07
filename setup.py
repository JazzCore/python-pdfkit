import codecs
from distutils.core import setup
import re
import pdfkit


def long_description():
    """Pre-process the README so that PyPi can render it properly."""
    with codecs.open('README.rst', encoding='utf8') as f:
        rst = f.read()
    code_block = '(:\n\n)?\.\. code-block::.*'
    rst = re.sub(code_block, '::', rst)
    return rst

setup(
    name='pdfkit',
    version=pdfkit.__version__,
    description=pdfkit.__doc__.strip(),
    long_description=long_description(),
    download_url='https://github.com/JazzCore/python-pdfkit',
    license=pdfkit.__license__,
    packages=['pdfkit'],
    author=pdfkit.__author__,
    author_email='stgolovanov@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XMl',
        'Topic :: Utilities'
        ]
)
