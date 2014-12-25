import unittest

from api.main import YQL


class YQLTest(unittest.TestCase):
    def setUp(self):
        self.yql = YQL()

    def test_appl(self):
        yql = YQL('AAPL', '2014-01-10', '2014-01-10')

        self.assertEqual(YQL.get_date('2014-01-10'), yql.get_prices()[0].get('date'))
        self.assertEqual('74.57', yql.get_prices()[0].get('price'))

        self.yql.select('AAPL', '2014-01-10', '2014-01-10')

        self.assertEqual(YQL.get_date('2014-01-10'), self.yql.get_prices()[0].get('date'))
        self.assertEqual('74.57', self.yql.get_prices()[0].get('price'))