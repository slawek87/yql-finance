import unittest

from api.main import YQL


class YQLTest(unittest.TestCase):
    def test_appl(self):
        yql_data = YQL.select('AAPL', '2014-01-10', '2014-01-10')

        self.assertEqual(YQL.to_date('2014-01-10'), yql_data[0].get('date'))
        self.assertEqual('74.57', yql_data[0].get('price'))

        yql_data = YQL('AAPL', '2014-01-10', '2014-01-10')

        self.assertEqual(YQL.to_date('2014-01-10'), yql_data[0].get('date'))
        self.assertEqual('74.57', yql_data[0].get('price'))