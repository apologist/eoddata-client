import os
import re
import datetime

import pytest

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

from eoddata_client import EodDataHttpClient, EodDataExchange, \
                           EodDataQuoteExtended, EodDataQuoteCompact, \
                           EodDataSymbol, EodDataSymbolCompact
from eoddata_client.eoddata_client import TestEnvironmentNotSet as \
    EnvironmentNotSet, PERIODS

BUSINESS_DAY_US = CustomBusinessDay(calendar=USFederalHolidayCalendar())

# get last business day in the USA (take into consideration US holidays)
TEST_DATE = datetime.date.today() - BUSINESS_DAY_US

# exclude month and weeks not to cause an error on small periods
TEST_PERIODS = [p[0] for p in PERIODS if p[0] not in ['m', 'w']]

TEST_EXCHANGE = 'nasdaq'

TEST_SYMBOLS = ['msft', 'amzn', 'aapl']


class TestClient(object):

    @pytest.fixture(scope='class')
    def client(self):
        try:
            client = EodDataHttpClient(os.environ['EOD_DATA_LOGIN'],
                                       os.environ['EOD_DATA_PASSWORD'])
        except KeyError:
            raise EnvironmentNotSet('Environment test variables not set. '
                                    'You should set `EOD_DATA_LOGIN` and '
                                    '`EOD_DATA_PASSWORD` to your EodData '
                                    'username and password accordingly.')
        client.login()
        return client

    def test_country_list(self, client):
        client.country_list()

    def test_data_client_latest_version(self, client):
        version = client.data_client_latest_version()
        assert re.match(r'(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(.){1,3}', version)

    @pytest.mark.skip(reason="not implemented yet")
    def test_data_formats(self, client):
        client.data_formats()

    def test_exchange_detail(self, client):
        for exchange in client.exchange_list():
            client.exchange_detail(exchange.code)

    def test_exchange_list(self, client):
        exchange_list = client.exchange_list()
        df = EodDataExchange.format(exchange_list, output_format='data-frame')
        assert len(df) == len(exchange_list)

    @pytest.mark.skip(reason="not implemented yet")
    def test_exchange_months(self, client):
        client.exchange_months()

    @pytest.mark.skip(reason="not implemented yet")
    def test_fundamental_list(self, client):
        client.fundamental_list()

    @pytest.mark.skip(reason="not implemented yet")
    def test_news_list(self, client):
        client.news_list()

    @pytest.mark.skip(reason="not implemented yet")
    def test_news_list_by_symbol(self, client):
        client.news_list_by_symbol()

    @pytest.mark.skip(reason="not implemented yet")
    def test_news_list_by_symbol(self, client):
        client.news_list_by_symbol()

    def test_quote_detail(self, client):
        client.quote_detail(TEST_EXCHANGE, TEST_SYMBOLS[0])

    def test_quote_list(self, client):
        quotes = client.quote_list(TEST_EXCHANGE)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame',
                                         df_index='Symbol')
        assert len(quotes) == len(df)

    def test_quote_list_specific(self, client):
        quotes = client.quote_list_specific(TEST_EXCHANGE,
                                            symbol_list=TEST_SYMBOLS)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame',
                                         df_index='Symbol')
        assert len(quotes) == len(df)

    def test_quote_list_by_date(self, client):
        quotes = client.quote_list_by_date(TEST_EXCHANGE, TEST_DATE)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame',
                                         df_index='Symbol')
        assert len(quotes) == len(df)

    def test_quote_list_by_date_compact(self, client):
        quotes = client.quote_list_by_date_compact(TEST_EXCHANGE, TEST_DATE)
        df = EodDataQuoteCompact.format(quotes, output_format='data-frame',
                                        df_index='Symbol')
        assert len(quotes) == len(df)

    @pytest.mark.parametrize('period', TEST_PERIODS)
    def test_quote_list_by_date_period(self, client, period):
        quotes = client.quote_list_by_date_period(TEST_EXCHANGE, TEST_DATE, period)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame',
                                         df_index='Symbol')
        assert len(quotes) == len(df)

    @pytest.mark.parametrize('period', TEST_PERIODS)
    def test_quote_list_by_date_period_compact(self, client, period):
        quotes = client\
            .quote_list_by_date_period_compact(TEST_EXCHANGE, TEST_DATE, period)
        df = EodDataQuoteCompact.format(quotes, output_format='data-frame',
                                        df_index='Symbol')
        assert len(quotes) == len(df)

    def test_symbol_history(self, client):
        quotes = client.symbol_history(TEST_EXCHANGE, TEST_SYMBOLS[0],
                                       datetime.date(1990, 1, 1))
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame')
        assert len(quotes) == len(df)

    @pytest.mark.parametrize('period', TEST_PERIODS)
    def test_symbol_history_period(self, client, period):
        business_day_2_weeks_ago = datetime.date.today() \
                                   - BUSINESS_DAY_US * 10
        quotes = client.symbol_history_period(TEST_EXCHANGE, TEST_SYMBOLS[0],
                                              business_day_2_weeks_ago, period)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame')
        assert len(quotes) == len(df)

    @pytest.mark.parametrize('period', TEST_PERIODS)
    def test_symbol_history_period_by_range(self, client, period):
        business_day_2_weeks_ago = datetime.date.today() \
                                   - BUSINESS_DAY_US * 10
        business_day_1_week_ago = datetime.date.today() - BUSINESS_DAY_US * 5

        quotes = client\
            .symbol_history_period_by_range(TEST_EXCHANGE, TEST_SYMBOLS[0],
                                            business_day_2_weeks_ago,
                                            business_day_1_week_ago, period)
        df = EodDataQuoteExtended.format(quotes, output_format='data-frame')
        assert len(quotes) == len(df)

    def test_symbol_list(self, client):
        symbols = client.symbol_list(TEST_EXCHANGE)
        df = EodDataSymbol.format(symbols, output_format='data-frame')
        assert len(symbols) == len(df)

    def test_symbol_list_compact(self, client):
        symbols = client.symbol_list_compact(TEST_EXCHANGE)
        df = EodDataSymbolCompact.format(symbols, output_format='data-frame')
        assert len(symbols) == len(df)
