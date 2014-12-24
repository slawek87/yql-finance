import datetime
from dateutil.relativedelta import relativedelta
import requests

ONE_YEAR = 1


class YQL(object):
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
        self.start_date = self.get_date(start_data)
        self.end_date = self.get_date(end_data)
        self.ticker = ticker

    @staticmethod
    def get_date(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def select(self, ticker, start_date, end_date):
        self.setup(ticker, start_date, end_date)

        data = self.get_chunk_data()

        self.data = data

        return self.data

    def prepare_query(self, start_date, end_date):
        query = \
            'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%s" and endDate = "%s"' \
            % (self.ticker, start_date, end_date)

        return query

    def send_request(self, query):
        self.parameters['q'] = query
        data = requests.get(self.api, params=self.parameters)

        return data.json()

    def get_chunk_data(self):
        if relativedelta(self.end_date, self.start_date).years <= ONE_YEAR:
            return self.get_data(self.start_date, self.end_date)

        data = []

        counter = ((relativedelta(self.end_date, self.start_date).years*12) / 6) + 1
        months = 0

        for month in range(counter):

            chunk_start_date = self.start_date+relativedelta(months=months)
            chunk_end_date = self.start_date+relativedelta(months=months+6)

            months += 6

            if chunk_end_date > self.end_date:
                chunk_end_date = self.end_date

            data = data + self.get_data(chunk_start_date, chunk_end_date)

        return data

    def get_data(self, start_date, end_date):
        query = self.prepare_query(start_date, end_date)
        response = self.send_request(query)

        return response['query']['results']['quote']

    def get_prices(self):
        prices = list()

        for item in self.data:
            date = datetime.datetime.strptime(item['Date'], '%Y-%m-%d')
            prices.append(dict(price=item['Close'], date=date))

        return prices


if __name__ == '__main__':
    yql = YQL('AAPL', '2011-01-01', '2014-12-31')
    #yql.select('AAPL', '2014-02-20', '2014-03-15')
    for item in yql.get_prices():
        print item.get('date'), item.get('price')