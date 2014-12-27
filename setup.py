# -*- coding: utf-8 -*-
from distutils.core import setup

try:
    with open('README.md', 'r') as f:
        readme = f.read()

    with open('LICENSE.txt', 'r') as f:
        license_ = f.read()
except:
    readme = ''
    license_ = ''

setup(
    name='yql-finance',
    version='0.1.0',
    packages=['yql'],
    url='',
    download_url='https://github.com/slawek87/yql-finance',
    license=license_,
    author=u'Sławomir Kabik',
    author_email='slawek@redsoftware.pl',
    description='yql-finance is simple and fast https://developer.yahoo.com/yql/console/ python API. API returns'
                'stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).',
    long_description=readme,
    keywords=['Python Yahoo YQL API', 'NASDAQ', 'S&P500', 'DAX', 'Python Stock prices'],
    install_requires=['setuptools', 'requests', 'python-dateutil'],
)
