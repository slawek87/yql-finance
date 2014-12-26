from yql.api import YQL


def fetch_appl():
    """Returns stock prices for Apple company."""
    yql = YQL('AAPL', '2014-01-01', '2014-01-10')

    for item in yql:
        print item.get('date'), item.get('price')

    yql.select('AAPL', '2014-01-01', '2014-01-10')

    for item in yql:
        print item.get('date'), item.get('price')


def fetch_googl():
    """Returns stock prices for Google company."""
    yql = YQL('GOOGL', '2014-01-01', '2014-01-10')

    for item in yql:
        print item.get('date'), item.get('price')

    yql.select('GOOGL', '2014-01-01', '2014-01-10')

    for item in yql:
        print item.get('date'), item.get('price')


if __name__ == '__main__':
    print "APPLE:"
    fetch_appl()

    print "\nGOOGLE:"
    fetch_googl()