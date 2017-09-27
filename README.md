<p align="center">
<em>Python http client to get market data from EodData Web Service.</em>
</p>

---

[![Build Status](https://travis-ci.org/apologist/eoddata-client.svg?branch=master)](https://travis-ci.org/apologist/eoddata-client)
[![Package version](https://badge.fury.io/py/eoddata-client.svg)](https://pypi.python.org/pypi/eoddata-client)


**Documentation**: [http://eoddata-client.readthedocs.io/](http://eoddata-client.readthedocs.io/)

**Requirements**: Python 3.5+, [requests](http://docs.python-requests.org/) and [pandas](http://pandas.pydata.org/)

## Quickstart

Install using `pip`:

```shell
$ pip install eoddata-client
```

Get data in pandas DataFrame:

```python
import os

from eoddata_client import EodDataHttpClient

client = EodDataHttpClient(os.environ['EOD_DATA_LOGIN'],
                           os.environ['EOD_DATA_PASSWORD'])

quotes = client.symbol_history('nasdaq', 'msft', datetime.date(1992, 1, 1))
quotes['Diff'] = quotes['Close'].shift(1) - quotes['Close']
print(quotes.tail())

#            Symbol   Open   High    Low  Close    Volume  Diff
# 2017-09-20   MSFT  75.35  75.55  74.31  74.94  21587800  0.50
# 2017-09-21   MSFT  75.11  75.24  74.11  74.21  19186100  0.73
# 2017-09-22   MSFT  73.99  74.51  73.85  74.41  14111300 -0.20
# 2017-09-25   MSFT  74.09  74.25  72.92  73.26  24149100  1.15
# 2017-09-26   MSFT  73.67  73.81  72.99  73.26  18019500  0.00
```

Or as regular collection of objects:

```python
import os

from eoddata_client import EodDataHttpClient

client = EodDataHttpClient(os.environ['EOD_DATA_LOGIN'],
                           os.environ['EOD_DATA_PASSWORD'])

quotes = client.symbol_history('nasdaq', 'msft', datetime.date(1992, 1, 1))
print(quotes[:2])
"""
[EodDataQuoteExtended(symbol=MSFT, quote_datetime=1992-01-01 00:00:00, open=2.319, high=2.319, low=2.319, close=2.319, volume=0, open_interest=0, previous=0.0, change=0.0, bid=0.0, ask=0.0, previous_close=0.0, next_open=0.0, modified=0001-01-01 00:00:00, name=Microsoft Corp, description=Microsoft Corp),
 EodDataQuoteExtended(symbol=MSFT, quote_datetime=1992-01-02 00:00:00, open=2.308, high=2.392, low=2.282, close=2.377, volume=1551300, open_interest=0, previous=0.0, change=0.0, bid=0.0, ask=0.0, previous_close=0.0, next_open=0.0, modified=2008-12-27 12:51:50.413000, name=Microsoft Corp, description=Microsoft Corp)]
"""
```
