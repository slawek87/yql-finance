![Alt text](https://travis-ci.org/slawek87/yql-finance.svg?branch=master)  

What is yql-finance?
===========
yql-finance is simple and fast https://developer.yahoo.com/yql/console/ python API.
    API returns stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).
    Stock prices: NASDAQ, SP&500, DAX etc.

How to use it?
==============
You can use it to fetch data in one of two ways:

```python
yql = YQL('AAPL', '2011-01-01', '2014-12-31')
```
```python
yql = YQL()
yql.select('AAPL', '2011-01-01', '2014-12-31')
```

Examples
===============

1. First way:
```python
from yql.api import YQL

yql = YQL('AAPL', '2014-01-01', '2014-01-10')

for item in yql:
    print item.get('date'), item.get('price')
```
2. Second way:
```python
from yql.api import YQL

yql = YQL()

yql.select('AAPL', '2014-01-01', '2014-01-10')

for item in yql:
    print item.get('date'), item.get('price')
```
Output:
```
2014-01-10 74.57
2014-01-09 75.07
2014-01-08 76.04
2014-01-07 75.56
2014-01-06 76.10
2014-01-03 75.69
2014-01-02 77.39
```
