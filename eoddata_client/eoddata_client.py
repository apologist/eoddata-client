"""
EodData HTTP Client.
"""
import xml.etree.ElementTree as ET
import requests

from eoddata_client.business_entities import (
    EodDataExchange, EodDataQuoteCompact, EodDataQuoteExtended
)


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

MSG_SUCCESS = 'Success'
MSG_INVALID_TOKEN = 'Invalid Token'
MSG_NOT_LOGGED_IN = 'Not logged in'
MSG_INVALID_EXCHANGE_CODE = 'Invalid Exchange Code'
MSG_INVALID_SYMBOL_CODE = 'Invalid Symbol Code'


class Error(Exception):
    """Base error for this module."""


class EodDataHttpClient(object):
    """
    EodData web service client.
    
    Endpoints:
        CountryList - country_list;
        DataClientLatestVersion - data_client_latest_version;
        DataFormats - data_formats;
        ExchangeGet - exchange_detail;
        ExchangeList - exchange_list;
        ExchangeMonths - exchange_months;
        FundamentalList - fundamental_list;
        Login - login;
        NewsList - new_list;
        NewsListBySymbol - new_list_by_symbol;
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

    def get_params(self, additional=None):
        """
        Get dictionary with parameters for a request.
        
        Args:
            additional (dict or None): Additional parameters for a request.
        
        Returns:
            Dictionary with parameters for a request.
        """
        parameters = {'Token': self._token}
        if additional:
            parameters.update(additional)
        return parameters

    def login(self):
        """
        Login to EODData Financial Information Web Service. Used for Web Authentication.
        
        Returns:
            bool, whether authentication was successful or not.
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
        
        Returns:
            List of tuples with country code and country name. For example:
            
            [('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'),
             ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola')] 
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
        """
        Returns the latest version information of Data Client.
        
        Returns:
            String with the latest version of data client in format "MAJOR.MINOR.PATCH.HOTFIX".
        """
        response = requests.get(self._base_url + 'DataClientLatestVersion', params=self.get_params())
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            message = root.attrib['Message']
            if message == 'Success':
                version = root[0].text
                return version
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def data_formats(self):
        # TODO: add this endpoint
        pass

    def exchange_detail(self, exchange_code):
        """
        Get detailed information about an exchange.
        
        Returns:
            EodDataExchange object.
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
            elif message == MSG_INVALID_EXCHANGE_CODE:
                # TODO: add error
                raise Exception
            elif message == 'Not logged in' or message == 'Invalid Token':
                # try to get token again
                pass
        return None

    def exchange_list(self):
        """
        Get all available exchanges.
        
        Returns:
            list, EodData exchanges.
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

    def exchange_months(self):
        """
        Returns the number of Months history a user is allowed to download.
        """
        # TODO: add this endpoint
        raise NotImplementedError

    def fundamental_list(self):
        """
        Returns a complete list of fundamental data for an entire exchange.
        """
        # TODO: add this endpoint
        raise NotImplementedError

    def new_list(self, exchange_code):
        """
        Returns a list of News articles for an entire exchange.
        """
        # TODO: add this endpoint
        raise NotImplementedError

    def new_list_by_symbol(self, exchange_code):
        """
        Returns a list of News articles for a given Exchange and Symbol.
        """
        # TODO: add this endpoint
        raise NotImplementedError

    def quote_detail(self, exchange_code, symbol):
        """
        Get an end of day quote for a specific symbol.
        
        Returns:
            EodDataQuoteExtended object.
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
        Get a complete list of end of day quotes for an entire exchange.
        
        Returns:
            list, EodData extended quotes.
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
        Get end of day quotes for specific symbols.
        
        Args:
            exchange_code (str): Exchange code.
            symbol_list (list of str): Symbol list.
            
        Returns:
            list, EodData extended quotes.
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
        
        Args:
            exchange_code: Exchange code.
            date (datetime.date): Date.

        Returns:
            list, EodData extended quotes
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
        
        Returns:
            EodDataQuoteCompact object.
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
        
        Returns:
            EodDataQuoteExtended object.
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
        
        Returns:
            EodDataQuoteCompact object.
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
        
        Returns:
            EodDataQuoteExtended object.
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
        
        Returns:
            EodDataQuoteExtended object.
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
        
        Returns:
            EodDataQuoteExtended object.
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
