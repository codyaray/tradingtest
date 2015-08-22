from locale import format


class Action(object):

  def update(self, holding, portfolio):
    raise Exception("Must be implemented")

  def __eq__(self, other):
      return self.__dict__ == other.__dict__


class CashDividendAction(Action):
  """
  Handles cash dividends. Dividends may be reinvested or swept
  to a cash account. Allows for fractional share purchases.
  """
  def __init__(self, value, currency):
    self.value = value
    self.currency = currency

  def update(self, holding, portfolio):
    # Must adjust the share price before reinvesting dividends
    self._adjust_share_price(holding, portfolio)
    if not holding.reinvest_dividends:
      self._sweep_dividends_to_cash(holding, portfolio)
    else:
      self._reinvest_dividends(holding, portfolio)

  def _sweep_dividends_to_cash(self, holding, portfolio):
    """
    Sweep the dividends into the Money Market cash account, performing any necessary currency conversions.
    """
    value = portfolio.currency_converter.convert(self.value, self.currency, portfolio.cash_currency)
    total_distribution = value * holding.shares
    portfolio.cash_value += total_distribution

  def _reinvest_dividends(self, holding, portfolio):
    """
    Reinvest the dividends into the issuing stock.
    """
    # Dividends should be distributed in the holding currency, but just in case of a special distribution...
    value = portfolio.currency_converter.convert(self.value, self.currency, holding.currency)
    total_distribution = value * holding.shares
    shares_to_purchase = total_distribution / holding.price
    holding.shares += shares_to_purchase

  def _adjust_share_price(self, holding, portfolio):
    """
    Adjust the share price downward by the amount of the dividend to reflect the reduced market cap.
    """
    value = portfolio.currency_converter.convert(self.value, self.currency, holding.currency)
    holding.price -= value

  def __repr__(self):
    return format("%.2f %s/share", (self.value, self.currency), monetary=True)


class StockSplitAction(Action):
  """
  Handles stock splits and reverse splits. As a recapitalization of company assets, these do
  not affect proportional ownership in the company; the share price adjusts to compensate for
  the change in the number of shares owned.
  """
  def __init__(self, before, after):
    self.before = before
    self.after = after

  def update(self, holding, portfolio):
    multiple = self.after / float(self.before) # ex: 9 for 10 => if I had 10 shares I now have 9. multiple = 9/10 = 0.9
    holding.shares *= multiple
    holding.price /= multiple

  def __repr__(self):
    return "%d for %d" % (self.after, self.before)


class StockDividendAction(Action):
  """
  Handles stock dividends. As a recapitalization of company assets, these do
  not affect proportional ownership in the company; the share price adjusts to compensate for
  the change in the number of shares owned.
  """

  def __init__(self, amount):
    self.amount = amount

  def update(self, holding, portfolio):
    holding.shares *= self.amount
    holding.price /= self.amount

  def __repr__(self):
    return "%0.3f/share" % self.amount


class NameChangeAction(Action):
  """
  Updates a company's stock name.
  """
  def __init__(self, new_name):
    self.new_name = new_name

  def update(self, holding, portfolio):
    holding.description = self.new_name

  def __repr__(self):
    return "new name is \"%s\"" % self.new_name


class SymbolChangeAction(Action):
  """
  Updates a company's stock symbol.
  """
  def __init__(self, new_symbol):
    self.new_symbol = new_symbol

  def update(self, holding, portfolio):
    del portfolio.holdings[holding.symbol]
    portfolio.holdings[self.new_symbol] = holding
    holding.symbol = self.new_symbol

  def __repr__(self):
    return "new symbol is %s" % self.new_symbol


class CurrencyConverter(object):
  """
  Static currency conversions between USD, CAD, and GBP. In real life, this would
  be replaced with a (cached, periodically refreshed?) call to an external service.
  """

  CONVERSION_TABLE = {
        # USD                # CAD                  # GBP
    ('USD', 'USD'): 1.00, ('CAD', 'USD'): 0.76, ('GBp', 'USD'): 1.57,  # USD
    ('USD', 'CAD'): 1.32, ('CAD', 'CAD'): 1.00, ('GBp', 'CAD'): 2.07,  # CAD
    ('USD', 'GBp'): 0.64, ('CAD', 'GBp'): 0.48, ('GBp', 'GBp'): 1.00,  # GBP
  }

  @classmethod
  def convert(cls, value, from_currency, to_currency):
    return value * cls.CONVERSION_TABLE[(from_currency, to_currency)]
