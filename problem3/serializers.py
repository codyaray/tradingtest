from StringIO import StringIO
from _csv import writer
from csv import DictReader
from datetime import datetime
from locale import atof, atoi, format
import re
from problem3.actions import CashDividendAction, StockSplitAction, StockDividendAction, \
  SymbolChangeAction, NameChangeAction
from problem3.models import Holding, Portfolio, ActionRecord


class CsvPortfolioSerializer(object):
  """
  Marshalls {@link Portfolio}s to/from CSV.
  """

  @staticmethod
  def deserialize(iterable, currency_converter, reinvest_dividends=False):
    holdings = []
    for row in DictReader(iterable):
      holdings.append(Holding(row['Symbol'], row['Description'], row['Country'],
                              atoi(row['Shares']), atof(row['Price']), row['Currency'], reinvest_dividends))
    return Portfolio(holdings, currency_converter)

  @classmethod
  def serialize(cls, portfolio):
    output = StringIO()
    portfolio_writer = writer(output)
    portfolio_writer.writerow(['Symbol', 'Description', 'Country', 'Shares', 'Price', 'Currency', 'Total Value'])
    for h in portfolio.holdings.values():
      portfolio_writer.writerow([h.symbol, h.description, h.country, "%.2f" % h.shares, cls._format(h.price), h.currency, cls._format(h.total_value())])
    portfolio_writer.writerow(['CASH', 'Money Market Account', '-', '-', '-', portfolio.cash_currency, cls._format(portfolio.cash_value)])
    portfolio_writer.writerow(['TOTAL', '-', '-', '-', '-', portfolio.cash_currency, cls._format(portfolio.value())])
    return output

  @staticmethod
  def _format(value):
    return format("%.2f", value, grouping=True)


class CsvActionsSerializer(object):
  """
  Marshalls {@link Action}s from CSV.
  """

  @staticmethod
  def deserialize(iterable, date_format="%m/%d/%Y"):
    actions = []
    for row in DictReader(iterable):
      actions.append(ActionRecord(datetime.strptime(row['Day'], date_format).date(), row['Symbol'], row['Corporate Action'].strip()))
    # Hack alert! Sort by date then description so "symbol change" is at the end for each day.
    return sorted(actions, key=lambda action: (action.date, action.description))


class ActionParser(object):
  """
  Parses {@link ActionRecord} descriptions into the appropriate {@link Action} object.
  """

  AVAILABLE_ACTIONS = {
    'cash_dividend': "Cash dividend - ",
    'split': "Stock split - ",
    'symbol_change': "Symbol change - ",
    'name_change': "Name change - ",
    'stock_dividend': "Stock dividend - "
  }

  @classmethod
  def parse(cls, description):
    for action, prefix in cls.AVAILABLE_ACTIONS.iteritems():
      if description.startswith(prefix):
        parse_action = getattr(cls, '_parse_%s' % action)
        return parse_action(description[len(prefix):])

  @staticmethod
  def _parse_cash_dividend(description):
    value, currency = description[:-len("/share")].split(' ')
    return CashDividendAction(float(value), currency)

  @staticmethod
  def _parse_split(description):
    return StockSplitAction(*reversed([int(n) for n in description.split(' for ')]))

  @staticmethod
  def _parse_symbol_change(description):
    return SymbolChangeAction(description[len("new symbol is "):])

  @staticmethod
  def _parse_name_change(description):
    return NameChangeAction(re.match('new name is "(.*)"', description).group(1))

  @staticmethod
  def _parse_stock_dividend(description):
    return StockDividendAction(float(description[:-len("/share")]))
