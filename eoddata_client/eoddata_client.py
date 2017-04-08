"""
EodData HTTP Client.
"""
import datetime
import xml.etree.ElementTree as ET
import requests


PERIODS = (
    ('1', 'One minute'),
    ('5', 'Five minutes'),
    ('10', 'Ten minutes'),
    ('15', 'Fifteen minutes'),
    ('30', 'Thirty minutes'),
    ('h', 'Hour'),
    ('d', 'Day'),
    ('w', 'Week'),
    ('m', 'Month'),
)


def string_to_datetime(iso8601_datetime_string):
    """Converts ISO 8601 datetime string to Python datetime"""
    try:
        return datetime.datetime.strptime(iso8601_datetime_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return datetime.datetime.strptime(iso8601_datetime_string, '%Y-%m-%dT%H:%M:%S.%f')


class EodDataExchange(object):
    """
    EodData Exchange entity.
    """

    def __init__(self, code, name, last_trade_time,
                 country_code, currency, advances, declines,
                 timezone, suffix='', is_intraday=False,
                 intraday_start_date=None, has_intraday=False):
        self.code = code
        """Exchange code"""
        self.name = name
        """Exchange full name"""
        self.last_trade_time = last_trade_time
        """Datetime of the last trade"""
        self.country_code = country_code
        """Code of the country where this exchnange is situated"""
        self.currency = currency
        """Exchange currency"""
        self.advances = advances
        self.declines = declines
        self.suffix = suffix
        self.timezone = timezone
        """Exchange timezone"""
        self.is_intraday = is_intraday
        """Availability of intraday data."""
        self.intraday_start_date = intraday_start_date
        """From what hat period is intraday data is available."""
        self.has_intraday = has_intraday
        """Indicates if EodData has intraday data for this exchange"""

    @classmethod
    def from_xml(cls, xml_exchange):
        """
        Get EodDataExchange object from xml element.
        :return: EodDataExchange object
        """
        exchange_dict = xml_exchange.attrib
        return cls(
            code=exchange_dict['Code'],
            name=exchange_dict['Name'],
            last_trade_time=string_to_datetime(exchange_dict['LastTradeDateTime']),
            country_code=exchange_dict['Country'],
            currency=exchange_dict['Currency'],
            advances=int(exchange_dict['Advances']),
            declines=int(exchange_dict['Declines']),
            suffix=exchange_dict['Suffix'],
            timezone=exchange_dict['TimeZone'],
            intraday_start_date=string_to_datetime(exchange_dict['IntradayStartDate']),
            is_intraday=bool(exchange_dict['IsIntraday']),
            has_intraday=bool(exchange_dict['HasIntradayProduct'])
        )

    def __str__(self):
        return self.code


class EodDataQuoteCompact(object):
    """
    EodData quote entity.
    """
    def __init__(self, symbol, quote_datetime,
                 open_price, high, low, close,
                 volume, open_interest, before,
                 after):
        self.symbol = symbol
        """Security symbol"""
        self.quote_datetime = quote_datetime
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.open_interest = open_interest
        self.before = before
        self.after = after

    @classmethod
    def from_xml(cls, xml_quote):
        """
        EodData extended quote entity.
        """
        quote_dict = xml_quote.attrib
        return cls(
            symbol=quote_dict['s'],
            quote_datetime=string_to_datetime(quote_dict['d']),
            open_price=float(quote_dict['o']),
            high=float(quote_dict['h']),
            low=float(quote_dict['l']),
            close=float(quote_dict['c']),
            volume=int(quote_dict['v']),
            open_interest=int(quote_dict['i']),
            before=float(quote_dict['b']),
            after=float(quote_dict['a']),
        )

    def __str__(self):
        return '{0} | {1}'.format(self.symbol, str(self.quote_datetime))


class EodDataQuoteExtended(object):
    """
    Get EodDataQuoteExtended object from xml element.
    :return: EodDataQuoteExtended object
    """

    def __init__(self, symbol, quote_datetime,
                 open_price, high, low, close, volume,
                 open_interest, previous, change,
                 bid, ask, modified, previous_close=0,
                 next_open=0, name='', description=''):
        self.symbol = symbol
        self.quote_datetime = quote_datetime
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.open_interest = open_interest
        self.previous = previous
        self.change = change
        self.bid = bid
        self.ask = ask
        self.modified = modified
        self.previous_close = previous_close
        self.next_open = next_open
        self.name = name
        self.description = description

    @classmethod
    def from_xml(cls, xml_quote):
        """
        Get EodDataQuoteExtended object from xml element.
        :return: EodDataQuoteExtended object
        """
        quote_dict = xml_quote.attrib
        return cls(
            symbol=quote_dict['Symbol'],
            quote_datetime=string_to_datetime(quote_dict['DateTime']),
            open_price=float(quote_dict['Open']),
            high=float(quote_dict['High']),
            low=float(quote_dict['Low']),
            close=float(quote_dict['Close']),
            volume=int(quote_dict['Volume']),
            open_interest=int(quote_dict['OpenInterest']),
            previous=float(quote_dict['Previous']),
            change=float(quote_dict['Change']),
            bid=float(quote_dict['Bid']),
            ask=float(quote_dict['Ask']),
            previous_close=float(quote_dict['PreviousClose']),
            next_open=float(quote_dict['NextOpen']),
            modified=string_to_datetime(quote_dict['Modified']),
            name=quote_dict['Name'],
            description=quote_dict['Description']
        )

    def __str__(self):
        return self.symbol


class EodDataHttpClient(object):
    """
    EodData web service client.
    Endpoints:
        Country - country_list;
        DataClientLatestVersion - data_client_latest_version;
        DataFormats - ;
        ExchangeGet - exchange_detail;
        ExchangeList - exchange_list;
        ExchangeMonths - ;
        FundamentalList - ;
        Login - login;
        NewsList - ;
        NewsListBySymbol - ;
        QuoteGet - quote_detail;
        QuoteList - quote_list;
        QuoteList2 - quote_list_specific;
        QuoteListByDate - quote_list_by_date;
        QuoteListByDate2 - quote_list_by_date_compact;
        QuoteListByDatePeriod - quote_list_by_date_period;
        QuoteListByDatePeriod2 - quote_list_by_date_period_compact;
        SplitListByExchange;
        SplitListBySymbol;
        SymbolChangesByExchange;
        SymbolChart;
        SymbolGet;
        SymbolHistory - symbol_history;
        SymbolHistoryPeriod - symbol_history_period;
        SymbolHistoryPeriodByDateRange - symbol_history_period;
        SymbolList;
        SymbolList2;
        TechnicalList;
        Top10Gains;
        Top10Losses;
        UpdateDataFormat;
        ValidateAccess.
    """

    _base_url = 'http://ws.eoddata.com/data.asmx/'

    def __init__(self, username, password, base_url=None):
        self._token = None
        self._username = username
        self._password = password
        if base_url:
            self._base_url = base_url

    def get_params(self, additional={}):
        """Dictionary with parameters for request."""
        parameters = {'Token': self._token}
        parameters.update(additional)
        return parameters

    def login(self):
        """
        Login to EODData Financial Information Web Service. Used for Web Authentication.
        """
        data = {
            'Username': self._username,
            'Password': self._password
        }
        response = requests.post(self._base_url + 'Login', data=data)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            if 'Token' in root.attrib:
                self._token = root.attrib['Token']
                # TODO: only for test purpose
                print(self._token)
                return True
        return False

    def country_list(self):
        """
        Returns a list of available countries.
        :return: list<tuple(country_code, country_name)>
        """
        response = requests.get(self._base_url + 'CountryList', params=self.get_params())
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                countries_element = root[0]
                countries = []
                for country in countries_element:
                    countries.append((country.attrib['Code'], country.attrib['Name']))
                return countries
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def data_client_latest_version(self):
        """Returns the latest version information of Data Client."""
        response = requests.get(self._base_url + 'DataClientLatestVersion', params=self.get_params())
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                dictionary = {}
                # TODO: fix
                for child in root:
                    dictionary[child.tag] = child.attrib
                return dictionary
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def exchange_detail(self, exchange_code):
        """
        Get detailed information of a specific exchange.
        :return: EodDataExchange instance or None.
        """
        additional = {'Exchange': exchange_code.upper()}
        response = requests.get(self._base_url + 'ExchangeGet', params=self.get_params(additional))
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                exchange_element = root[0]
                exchange = EodDataExchange.from_xml(exchange_element)
                return exchange
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def exchange_list(self):
        """
        Get all available exchanges.
        :return: list<EodDataExchange>
        """
        response = requests.get(self._base_url + 'ExchangeList', params=self.get_params())
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                exchanges_xml = list(root[0])
                exchanges = []
                for exchange_xml in exchanges_xml:
                    exchange = EodDataExchange.from_xml(exchange_xml)
                    exchanges.append(str(exchange))
                return exchanges
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def quote_detail(self, exchange_code, symbol):
        """
        Get an end of day quote for a specific symbol.
        :return: EodDataQuoteExtended or None
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'Symbol': symbol.upper()
        }
        response = requests.get(self._base_url + 'QuoteGet', params=self.get_params(additional))
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quote_xml = [el for el in list(root) if el.tag.endswith('QUOTE')][0]
                quote = EodDataQuoteExtended.from_xml(quote_xml)
                return quote
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def quote_list(self, exchange_code):
        """
        Get complete list of end of day quotes for an entire exchange.
        :return: list<EodDataQuoteExtended> or None.
        """
        additional = {
            'Exchange': exchange_code.upper()
        }
        response = requests.get(self._base_url + 'QuoteList', params=self.get_params(additional))
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None


    def quote_list_specific(self, exchange_code, symbol_list):
        """
        Get an end of day quote for specific symbols.
        :return: list<EodDataQuoteExtended> instance or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'Symbols': ','.join(symbol_list)
        }
        response = requests.get(self._base_url + 'QuoteList2', params=self.get_params(additional))
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def quote_list_by_date(self, exchange_code, date):
        """
        Get a complete list of end of day quotes for an entire exchange and a specific date.
        :return: list<EodDataQuoteExtended> or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'QuoteDate': date.strftime('%Y%m%d'),
        }
        response = requests.get(
            self._base_url + 'QuoteListByDate',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def quote_list_by_date_compact(self, exchange_code, date):
        """
        Get a complete list of end of day quotes for an entire exchange and a specific date (compact format).
        :return: list<EodDataQuoteCompact> or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'QuoteDate': date.strftime('%Y%m%d'),
        }
        response = requests.get(
            self._base_url + 'QuoteListByDate2',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES2')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteCompact.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None


    def quote_list_by_date_period(self, exchange_code, date, period):
        """
        Get a complete list of end of day quotes for an entire exchange and a specific date (compact format).
        :return:  list<EodDataQuoteExtended> or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'QuoteDate': date.strftime('%Y%m%d'),
            'Period': period
        }
        response = requests.get(
            self._base_url + 'QuoteListByDatePeriod',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def quote_list_by_date_period_compact(self, exchange_code, date, period):
        """
        Get a complete list of end of day quotes for an entire exchange and a specific date (compact format).
        :return: list<EodDataQuoteCompact> or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'QuoteDate': date.strftime('%Y%m%d'),
            'Period': period
        }
        response = requests.get(
            self._base_url + 'QuoteListByDatePeriod2',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES2')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteCompact.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def symbol_history(self, exchange_code, symbol, start_date):
        """
        Get a list of historical end of day data of a specified symbol and specified start date up to today's date.
        :return: list<EodDataQuoteExtended> or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'StartDate': start_date.strftime('%Y%m%d'),
            'Symbol': symbol.upper()
        }
        response = requests.get(
            self._base_url + 'SymbolHistory',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def symbol_history_period(self, exchange_code, symbol, date, period):
        """
        Get a list of historical data of a specified symbol, specified date and specified period.
        :return: list<EodDataQuoteExtended> object or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'Date': date.strftime('%Y%m%d'),
            'Symbol': symbol.upper(),
            'Period': period
        }
        response = requests.get(
            self._base_url + 'SymbolHistoryPeriod',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def symbol_history_period_by_range(self, exchange_code, symbol, start_date, end_date, period):
        """
        Get a list of historical data of a specified symbol, specified date range and specified period.
        :return: EodDataQuote object or None.
        """
        additional = {
            'Exchange': exchange_code.upper(),
            'StartDate': start_date.strftime('%Y%m%d'),
            'EndDate': end_date.strftime('%Y%m%d'),
            'Symbol': symbol.upper(),
            'Period': period
        }
        response = requests.get(
            self._base_url + 'SymbolHistoryPeriod',
            params=self.get_params(additional)
        )
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                quotes_xml = [el for el in list(root) if el.tag.endswith('QUOTES')][0]
                quotes = []
                for quote_xml in list(quotes_xml):
                    quote = EodDataQuoteExtended.from_xml(quote_xml)
                    quotes.append(quote)
                return quotes
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None
