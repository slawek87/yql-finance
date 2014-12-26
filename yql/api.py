import datetime
from dateutil.relativedelta import relativedelta

from yql.request import Request
from yql import const


class YQL(object):
    """yql-finance is simple and fast https://developer.yahoo.com/yql/console/ python API.
    API returns stock closing prices for current period of time and current stock ticker/symbol (i.e. APPL, GOOGL).

    You can use it to fetch data in one of two ways::
        - yql = YQL('AAPL', '2011-01-01', '2014-12-31')
        or
        - yql = YQL()
          yql.select('AAPL', '2011-01-01', '2014-12-31')

    Requirements:
        - requests
        - dateutil
    """
    request = Request()

    def __repr__(self):
        return '<YQL Object: symbol %s start_date / %s end_date %s>' % (self.symbol, self.start_date, self.end_date)

    def __init__(self, symbol, start_data, end_data):
        """Method setups basic (self) variables."""
        self.start_date = self.to_date(start_data)
        self.end_date = self.to_date(end_data)
        self.symbol = symbol

        self.data = self.fetch_data()

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    @staticmethod
    def to_date(date):
        """Method converts string date to datetime date. You should use %Y-%m-%d format."""
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()

    @classmethod
    def select(cls, symbol, start_date, end_date):
        """Method returns stock prices for current: ticker/symbol, start date, end date."""
        instance = cls(symbol, start_date, end_date)

        return instance.data

    def fetch_data(self):
        """Method returns results from response of Yahoo YQL API. It should returns always python list."""
        if relativedelta(self.end_date, self.start_date).years <= const.ONE_YEAR:
            data = self.request.send(self.symbol, self.start_date, self.end_date)
        else:
            data = self.fetch_chunk_data()

        return self.clean(data)

    def fetch_chunk_data(self):
        """If period of time between start end end is bigger then one year
        We have to create and fetch chunks dates (6 months chunks)."""
        data = []

        counter = (relativedelta(self.end_date, self.start_date).months / 6) + 1
        months = 0

        for month in range(counter):

            chunk_start_date = self.start_date + relativedelta(months=months)
            chunk_end_date = self.start_date + relativedelta(months=months + 6)

            months += 6

            if chunk_end_date > self.end_date:
                chunk_end_date = self.end_date

            data = data + self.request.send(self.symbol, chunk_start_date, chunk_end_date)

        return data

    def clean(self, data):
        """Method returns cleaned list of stock closing prices
        (i.e. dict(date=datetime.date(2015, 1, 2), price='23.21'))."""
        cleaned_data = list()

        if not isinstance(data, list):
            data = [data]

        for item in data:
            date = datetime.datetime.strptime(item['Date'], '%Y-%m-%d').date()
            cleaned_data.append(dict(price=item['Adj_Close'], date=date))

        return cleaned_data
