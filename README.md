yql-finance
===========
yql-finance is simple and fast https://developer.yahoo.com/yql/console/ python API.
    API returns fetched stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).

You can fetch data one of two ways:
        `yql = YQL('AAPL', '2011-01-01', '2014-12-31')`
    or
        `yql = YQL()`
        `yql.select('AAPL', '2011-01-01', '2014-12-31')`

To get prices use `get_prices()` method. It returns list of stock closing prices for current period of time
and current ticker.
