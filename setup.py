import codecs
from distutils.core import setup
from setuptools.command.test import test as TestCommand
import re
import os
import sys
import pdfkit

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['pdfkit-tests.py']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        os.chdir('tests/')
        errno = pytest.main(self.test_args)
        sys.exit(errno)

def long_description():
    """Pre-process the README so that PyPi can render it properly."""
    with codecs.open('README.rst', encoding='utf8') as f:
        rst = f.read()
    code_block = '(:\n\n)?\.\. code-block::.*'
    rst = re.sub(code_block, '::', rst)
    return rst + '\n\n' + open('HISTORY.rst').read()

setup(
    name='pdfkit',
    version=pdfkit.__version__,
    description=pdfkit.__doc__.strip(),
    long_description=long_description(),
    download_url='https://github.com/JazzCore/python-pdfkit',
    license=pdfkit.__license__,
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    packages=['pdfkit'],
    author=pdfkit.__author__,
    author_email='stgolovanov@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities'
        ]
)
