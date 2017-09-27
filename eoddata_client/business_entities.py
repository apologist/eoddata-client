import logging

import pandas as pd

from eoddata_client.utils import string_to_datetime

logger = logging.getLogger(__name__)


class EodDataExchange(object):
    """EodData Exchange.

    Attributes:
        code (str): Exchange code
        name (str): Datetime of the last trade
        last_trade_time (datetime): Datetime of the last trade
        country_code (str): Code of the country where this exchange is situated
        currency (str): Exchange currency
        advances (int): Advances count
        declines (int): Declines count
        suffix (str): Exchange suffix
        timezone (str): Exchange timezone
        is_intraday (bool): Availability of intraday data.
        intraday_start_date (datetime or None): 
            Intraday data availability start date.
        has_intraday (bool): Indicates if EodData has intraday data 
            for this exchange.
    """

    def __init__(self, code, name, last_trade_time,
                 country_code, currency, advances, declines,
                 timezone, suffix='', is_intraday=False,
                 intraday_start_date=None, has_intraday=False):
        self.code = code
        self.name = name
        self.last_trade_time = last_trade_time
        self.country_code = country_code
        self.currency = currency
        self.advances = advances
        self.declines = declines
        self.suffix = suffix
        self.timezone = timezone
        self.is_intraday = is_intraday
        self.intraday_start_date = intraday_start_date
        self.has_intraday = has_intraday

    @classmethod
    def from_xml(cls, xml_exchange):
        """Get EodDataExchange object from xml element.
        
        Args:
            xml_exchange: Exchange XML element.
            
        Returns:
            EodDataExchange instance or None.
        """
        exchange_dict = xml_exchange.attrib
        try:
            return cls(
                code=exchange_dict['Code'],
                name=exchange_dict['Name'],
                last_trade_time=string_to_datetime(
                    exchange_dict['LastTradeDateTime']
                ),
                country_code=exchange_dict['Country'],
                currency=exchange_dict['Currency'],
                advances=int(exchange_dict['Advances']),
                declines=int(exchange_dict['Declines']),
                suffix=exchange_dict['Suffix'],
                timezone=exchange_dict['TimeZone'],
                intraday_start_date=string_to_datetime(
                    exchange_dict['IntradayStartDate']
                ),
                is_intraday=bool(exchange_dict['IsIntraday']),
                has_intraday=bool(exchange_dict['HasIntradayProduct'])
            )
        except KeyError:
            logger.exception('Missing attribute in XML element.')
        except:
            logger.exception('Unexpected error.')

    def to_dict(self):
        return {
            'Name': self.name,
            'Last Trade Time': self.last_trade_time,
            'Country Code': self.country_code,
            'Currency': self.currency,
            'Advances': self.advances,
            'Declines': self.declines,
            'Timezone': self.timezone,
            'Intraday Start Date': self.intraday_start_date,
            'Is Intraday': self.is_intraday,
            'Has Intraday': self.has_intraday
        }

    @classmethod
    def list_to_df(cls, exchange_list):
        data = [exchange.to_dict() for exchange in exchange_list]
        index = [exchange.code for exchange in exchange_list]
        return pd.DataFrame(data=data, index=index)

    @classmethod
    def format(cls, exchange_list, input_format='entity-list',
               output_format=None):
        if output_format is None:
            return exchange_list
        elif input_format == output_format:
            return exchange_list
        elif input_format == 'entity-list' and output_format == 'data-frame':
            return cls.list_to_df(exchange_list)
        else:
            raise NotImplementedError

    def __repr__(self):
        return 'EodDataExchange(code={0}, name={1}, last_trade_time={2},' \
               'country_code={3}, currency={4}, advances={5}, declines={6}, ' \
               'suffix={7}, timezone={8}, intraday_start_date={9}, ' \
               'is_intraday={10}, has_intraday={11})'.format(
                    self.code, self.name, self.last_trade_time,
                    self.country_code, self.currency, self.advances,
                    self.declines, self.suffix, self.timezone,
                    self.intraday_start_date, self.is_intraday,
                    self.has_intraday
                )

    def __str__(self):
        return '%s (%s)' % (self.code, self.name)


class EodDataQuoteCompact(object):
    """EodData quote.

    Attributes:
        symbol (str): Symbol.
        quote_datetime (datetime): Quote datetime.
        open (float): Open price.
        high (float): High price.
        low (float): Low price.
        close (float): Close price.
        volume (int): Traded volume.
        open_interest (int): Open interest.
        before (float): 
        after (float):
    """

    def __init__(self, symbol, quote_datetime,
                 open, high, low, close,
                 volume, open_interest, before,
                 after):
        self.symbol = symbol
        """Security symbol"""
        self.quote_datetime = quote_datetime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.open_interest = open_interest
        self.before = before
        self.after = after

    @classmethod
    def from_xml(cls, xml_quote):
        """Get instance from xml.

        Returns:
            EodDataQuoteCompact instance or None.
        """
        quote_dict = xml_quote.attrib
        try:
            return cls(
                symbol=quote_dict['s'],
                quote_datetime=string_to_datetime(quote_dict['d']),
                open=float(quote_dict['o']),
                high=float(quote_dict['h']),
                low=float(quote_dict['l']),
                close=float(quote_dict['c']),
                volume=int(quote_dict['v']),
                open_interest=int(quote_dict['i']),
                before=float(quote_dict['b']),
                after=float(quote_dict['a']),
            )
        except KeyError:
            logger.exception('Missing attribute in XML element.')
        except:
            logger.exception('Unexpected error.')

    def to_dict(self):
        return {
            'Datetime': self.quote_datetime,
            'Symbol': self.symbol,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume

        }

    @classmethod
    def list_to_df(cls, quote_list, index_column='Datetime'):
        index = []
        data = []
        columns = ['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close',
                   'Volume']
        columns.remove(index_column)
        for quote in quote_list:
            d = quote.to_dict()
            index.append(d[index_column])
            del d[index_column]
            data.append(d)
        return pd.DataFrame(data=data, index=index,
                            columns=columns)

    @classmethod
    def format(cls, quote_list, input_format='entity-list', output_format=None,
               df_index='Datetime'):
        if output_format is None:
            return quote_list
        elif input_format == output_format:
            return quote_list
        if input_format == 'entity-list' and output_format == 'data-frame':
            return cls.list_to_df(quote_list, df_index)
        else:
            raise NotImplementedError

    def __repr__(self):
        return 'EodDataQuoteCompact(symbol={0}, quote_datetime={1}, open={2}, '\
               'high={3}, low={4}, close={5}, volume={6}, open_interest={7}, ' \
               'before={8}, after={9})'.format(
                    self.symbol, self.quote_datetime, self.open, self.high,
                    self.low, self.close, self.volume, self.open_interest,
                    self.before, self.after
               )

    def __str__(self):
        return '{0} | {1}'.format(self.symbol, str(self.quote_datetime))


class EodDataQuoteExtended(object):
    """EodData extended quote.

    Attributes:
        symbol (str): Symbol.
        quote_datetime (datetime): Quote datetime.
        open (float): Open price.
        high (float): High price.
        low (float): Low price.
        close (float): Close price.
        volume (int): Traded volume.
        open_interest (int): Open interest.
        previous (float): Previous close price. 
        change (float): Change from previous close.
        bid (float): Bid price.
        ask (float): Ask price.
        modified (datetime): Time of the last update for this security.
        name (str): Full name of a traded asset.
        description (str): Description.
        df_columns (tuple of str): Data frame columns (static attribute).
    """

    df_columns = ('Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close',
                  'Volume')

    def __init__(self, symbol, quote_datetime,
                 open, high, low, close, volume,
                 open_interest, previous, change,
                 bid, ask, modified, previous_close=0,
                 next_open=0, name='', description=''):
        self.symbol = symbol
        self.quote_datetime = quote_datetime
        self.open = open
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
        """Get EodDataQuoteExtended object from xml element.

        Returns:
            EodDataQuoteExtended instance or None.
        """
        quote_dict = xml_quote.attrib
        try:
            return cls(
                symbol=quote_dict['Symbol'],
                quote_datetime=string_to_datetime(quote_dict['DateTime']),
                open=float(quote_dict['Open']),
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
        except KeyError:
            logger.exception('Missing attribute in XML element.')
        except:
            logger.exception('Unexpected error.')

    def to_dict(self):
        return {
            'Datetime': self.quote_datetime,
            'Symbol': self.symbol,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
            'Name': self.name
        }

    @classmethod
    def list_to_df(cls, quote_list, index_column='Datetime'):
        index = []
        data = []
        columns = list(cls.df_columns)
        columns.remove(index_column)
        for quote in quote_list:
            d = quote.to_dict()
            index.append(d[index_column])
            del d[index_column]
            data.append(d)
        return pd.DataFrame(data=data, index=index,
                            columns=columns)

    @classmethod
    def format(cls, quote_list, input_format='entity-list', output_format=None,
               df_index='Datetime'):
        if output_format is None:
            return quote_list
        elif input_format == output_format:
            return quote_list
        if input_format == 'entity-list' and output_format == 'data-frame':
            return cls.list_to_df(quote_list, index_column=df_index)
        else:
            raise NotImplementedError

    def __repr__(self):
        return 'EodDataQuoteExtended(symbol={0}, quote_datetime={1}, open={2},'\
               ' high={3}, low={4}, close={5}, volume={6}, open_interest={7}, '\
               'previous={8}, change={9}, bid={10}, ask={11}, ' \
               'previous_close={12}, next_open={13}, modified={14}, name={15},'\
               ' description={16})'.format(
                self.symbol, self.quote_datetime, self.open, self.high,
                self.low, self.close, self.volume, self.open_interest,
                self.previous, self.change, self.bid, self.ask,
                self.previous_close, self.next_open, self.modified, self.name,
                self.description
                )

    def __str__(self):
        return '{0} | {1}'.format(self.symbol, str(self.quote_datetime))


class EodDataSymbol(object):
    """EodData symbol.

    Attributes:
        code (str): Symbol code.
        name (str): Asset name.
        long_name (str): Long name.
    """
    def __init__(self, code, name, long_name):
        self.code = code
        self.name = name
        self.long_name = long_name

    @classmethod
    def from_xml(cls, xml_symbol):
        """Get EodDataSymbol object from xml element.

        Returns:
            EodDataSymbol instance or None.
        """
        symbol_dict = xml_symbol.attrib
        try:
            return cls(
                code=symbol_dict['Code'],
                name=symbol_dict['Name'],
                long_name=symbol_dict['LongName']
            )
        except KeyError:
            logger.exception('Missing attribute in XML element.')
        except:
            logger.exception('Unexpected error.')

    def to_dict(self):
        return {
            'Code': self.code,
            'Name': self.name,
            'LongName': self.long_name
        }

    @classmethod
    def list_to_df(cls, quote_list, index_column='Code'):
        index = []
        data = []
        columns = ['Code', 'Name', 'LongName']
        columns.remove(index_column)
        for quote in quote_list:
            d = quote.to_dict()
            index.append(d[index_column])
            del d[index_column]
            data.append(d)
        return pd.DataFrame(data=data, index=index,
                            columns=columns)

    @classmethod
    def format(cls, quote_list, input_format='entity-list', output_format=None,
               df_index='Code'):
        if output_format is None:
            return quote_list
        elif input_format == output_format:
            return quote_list
        if input_format == 'entity-list' and output_format == 'data-frame':
            return cls.list_to_df(quote_list, index_column=df_index)
        else:
            raise NotImplementedError

    def __repr__(self):
        return 'EodDataSymbol(code={0}, name={1}, long_name={2})'.format(
            self.code, self.name, self.long_name
        )

    def __str__(self):
        return '{0} | {1}'.format(self.code, self.name)


class EodDataSymbolCompact(object):
    """EodData symbol (compact).

    Attributes:
        code (str): Symbol code.
        name (str): Asset name.
    """
    def __init__(self, code, name):
        self.code = code
        self.name = name

    @classmethod
    def from_xml(cls, xml_symbol):
        """Get EodDataSymbolCompact object from xml element.

        Returns:
            EodDataSymbolCompact instance or None.
        """
        symbol_dict = xml_symbol.attrib
        try:
            return cls(
                code=symbol_dict['c'],
                name=symbol_dict['n'],
            )
        except KeyError:
            logger.exception('Missing attribute in XML element.')
        except:
            logger.exception('Unexpected error.')

    def to_dict(self):
        return {
            'Code': self.code,
            'Name': self.name
        }

    @classmethod
    def list_to_df(cls, quote_list, index_column='Code'):
        index = []
        data = []
        columns = ['Code', 'Name']
        columns.remove(index_column)
        for quote in quote_list:
            d = quote.to_dict()
            index.append(d[index_column])
            del d[index_column]
            data.append(d)
        return pd.DataFrame(data=data, index=index,
                            columns=columns)

    @classmethod
    def format(cls, quote_list, input_format='entity-list', output_format=None,
               df_index='Code'):
        if output_format is None:
            return quote_list
        elif input_format == output_format:
            return quote_list
        if input_format == 'entity-list' and output_format == 'data-frame':
            return cls.list_to_df(quote_list, index_column=df_index)
        else:
            raise NotImplementedError

    def __repr__(self):
        return 'EodDataSymbol(code={0}, name={1}'.format(
            self.code, self.name
        )

    def __str__(self):
        return '{0} | {1}'.format(self.code, self.name)
