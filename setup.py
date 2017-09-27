import os
import re

from setuptools import setup


try:
    from pypandoc import convert

    if os.name == 'nt':
        os.environ.setdefault('PYPANDOC_PANDOC',
                              'c:\\Program Files (x86)\\Pandoc\\pandoc.exe')

    def read_md(f):
        return convert(f, 'rst', format='md')
except ImportError:
    print('warning: pypandoc module not found, '
          'could not convert Markdown to RST')

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

VERSION = get_version('eoddata_client')

setup(
    name='eoddata_client',
    packages=['eoddata_client'],
    version=VERSION,
    description='Client to get historical market data from EODData web service.',
    long_description=read_md('README.md'),
    author='Aleksey',
    author_email='quant@apologist.io',
    url='https://github.com/apologist/eoddata-client',
    license='Public Domain',
    download_url='',
    keywords=['market', 'data', 'trading', 'stocks', 'finance'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['requests', 'pandas'],
)
