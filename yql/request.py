import requests


class Request(object):
    """Class is responsible for prepare request query and sends it to YQL Yahoo API."""
    parameters = {
        'q': '',
        'format': 'json',
        'diagnostics': 'false',
        'env': 'store://datatables.org/alltableswithkeys',
        'callback': ''
    }
    api = 'https://query.yahooapis.com/v1/public/yql'

    def prepare_query(self, symbol,  start_date, end_date):
        """Method returns prepared request query for Yahoo YQL API."""
        query = \
            'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%s" and endDate = "%s"' \
            % (symbol, start_date, end_date)

        return query

    def send(self, symbol, start_date, end_date):
        """Method sends request to Yahoo YQL API."""
        query = self.prepare_query(symbol, start_date, end_date)

        self.parameters['q'] = query
        response = requests.get(self.api, params=self.parameters).json()

        results = response['query']['results']['quote']

        return results
