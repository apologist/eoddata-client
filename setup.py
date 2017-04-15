from setuptools import setup

setup(
    name='eoddata_client',
    packages=['eoddata_client'],
    version='0.3.0',
    description='Client to get historical market data from EODData web service.',
    author='Aleksey',
    author_email='apologist.code@gmail.com',
    url='https://github.com/apologist/eoddata-client',
    license='Public Domain',
    download_url='',
    keywords=['market', 'data', 'trading', 'stocks', 'finance'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['requests'],
)
