import datetime
from dateutil.relativedelta import relativedelta
import requests

ONE_YEAR = 1


class YQL(object):
    """yql-finance is simple and fast https://developer.yahoo.com/yql/console/ python API.
    API returns fetched stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).

    You can fetch data one of two ways:
        - yql = YQL('AAPL', '2011-01-01', '2014-12-31')
        or
        - yql = YQL()
          yql.select('AAPL', '2011-01-01', '2014-12-31')

    To get prices use `get_prices()` method. It returns list of stock closing prices for current period of time
    and current ticker.

    Requirements:
        - requests
        - dateutil
    """
    parameters = {
        'q': '',
        'format': 'json',
        'diagnostics': 'true',
        'env': 'store://datatables.org/alltableswithkeys',
        'callback': ''
    }
    api ='https://query.yahooapis.com/v1/public/yql'

    data = []

    start_date = None
    end_date = None

    ticker = None

    def __init__(self, ticker=None, start_date=None, end_date=None):
        if start_date and end_date and ticker:
            self.select(ticker, start_date, end_date)

    def setup(self, ticker, start_data, end_data):
        """Method setups basic (self) variables."""
        self.start_date = self.get_date(start_data)
        self.end_date = self.get_date(end_data)
        self.ticker = ticker

    @staticmethod
    def get_date(date):
        """Method converts string date to datetime date. You should use %Y-%m-%d format."""
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def select(self, ticker, start_date, end_date):
        """Method returns stock prices for current: ticker, start date, end date."""
        self.setup(ticker, start_date, end_date)

        data = self.fetch_chunks_data()

        self.data = data

        return self.data

    def prepare_query(self, start_date, end_date):
        """Method returns prepared request query for Yahoo YQL API."""
        query = \
            'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%s" and endDate = "%s"' \
            % (self.ticker, start_date, end_date)

        return query

    def send_request(self, query):
        """Method sends request to Yahoo YQL API."""
        self.parameters['q'] = query
        data = requests.get(self.api, params=self.parameters)

        return data.json()

    def fetch_chunks_data(self):
        """If period of time between start end end is bigger then one year
        We have to create and fetch chunks dates (6 months chunks)."""
        if relativedelta(self.end_date, self.start_date).years <= ONE_YEAR:
            return self.fetch_data(self.start_date, self.end_date)

        data = []

        counter = ((relativedelta(self.end_date, self.start_date).years*12) / 6) + 1
        months = 0

        for month in range(counter):

            chunk_start_date = self.start_date+relativedelta(months=months)
            chunk_end_date = self.start_date+relativedelta(months=months+6)

            months += 6

            if chunk_end_date > self.end_date:
                chunk_end_date = self.end_date

            data = data + self.fetch_data(chunk_start_date, chunk_end_date)

        return data

    def fetch_data(self, start_date, end_date):
        """Method returns json results from response of Yahoo YQL API."""
        query = self.prepare_query(start_date, end_date)
        response = self.send_request(query)

        return response['query']['results']['quote']

    def get_prices(self):
        """Method returns list of stock closing prices (i.e. ['2015-01-02', '23.21'])."""
        prices = list()

        for data in self.data:
            date = datetime.datetime.strptime(data['Date'], '%Y-%m-%d')
            prices.append(dict(price=data['Close'], date=date))

        return prices