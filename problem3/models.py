class Portfolio(object):

  def __init__(self, holdings, currency_converter, cash_value=0.0, cash_currency='USD'):
    self.holdings = {holding.symbol: holding for holding in holdings}
    self.cash_value = cash_value
    self.cash_currency = cash_currency
    self.currency_converter = currency_converter

  def value(self):
    holdings_value = sum([self.currency_converter.convert(h.total_value(), h.currency, self.cash_currency)
                          for h in self.holdings.values()])
    return self.cash_value + holdings_value

class Holding(object):

  def __init__(self, symbol, description, country, shares, price, currency, reinvest_dividends=False):
    self.symbol = symbol
    self.description = description
    self.country = country
    self.shares = shares
    self.price = price
    self.currency = currency
    self.reinvest_dividends = reinvest_dividends

  def total_value(self):
    return self.shares * self.price

  def __repr__(self):
    return "Holding<%s, %d shares, %0.2f/share, %s %s total value>" % \
           (self.symbol, self.shares, self.price, self.total_value(), self.currency)

class ActionRecord(object):

  def __init__(self, date, symbol, description):
    self.date = date
    self.symbol = symbol
    self.description = description

  def __repr__(self):
    return "Action<date=%s, symbol=%s, description=%s>" % (self.date, self.symbol, self.description)