from unittest import TestCase
from problem3.actions import CashDividendAction, StockSplitAction, StockDividendAction, NameChangeAction, SymbolChangeAction, CurrencyConverter
from problem3.models import Holding, Portfolio


class CashDividendActionTest(TestCase):

  CONVERTER = CurrencyConverter()

  def test_update_reinvest_dividends(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD', reinvest_dividends=True)
    portfolio = Portfolio([holding], self.CONVERTER)
    sut = CashDividendAction(1.50, 'USD')
    sut.update(holding, portfolio)
    self.assertEqual(8.50, holding.price)
    self.assertEqual(120*(1+1.5/8.5), holding.shares)
    self.assertEqual(0, portfolio.cash_value)

  def test_update_sweep_dividends(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD', reinvest_dividends=False)
    portfolio = Portfolio([holding], self.CONVERTER)
    sut = CashDividendAction(1.50, 'USD')
    sut.update(holding, portfolio)
    self.assertEqual(8.50, holding.price)
    self.assertEqual(120, holding.shares)
    self.assertEqual(180, portfolio.cash_value)

  def test_update_sweep_dividends_another_currency(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD', reinvest_dividends=False)
    portfolio = Portfolio([holding], self.CONVERTER)
    sut = CashDividendAction(1.50, 'CAD')
    distribution = 1.50 * self.CONVERTER.CONVERSION_TABLE[('CAD', 'USD')]
    new_share_price = 10 - distribution
    sut.update(holding, portfolio)
    self.assertEqual(new_share_price, holding.price)
    self.assertEqual(120, holding.shares)
    self.assertEqual(120 * distribution, portfolio.cash_value)

  def test_update_reinvest_dividends_another_currency(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD', reinvest_dividends=True)
    portfolio = Portfolio([holding], self.CONVERTER)
    sut = CashDividendAction(1.50, 'CAD')
    distribution = 1.50 * self.CONVERTER.CONVERSION_TABLE[('CAD', 'USD')]
    new_share_price = 10 - distribution
    sut.update(holding, portfolio)
    self.assertEqual(new_share_price, holding.price)
    self.assertEqual(120*(1+distribution/new_share_price), holding.shares)
    self.assertEqual(0, portfolio.cash_value)

class StockSplitActionTest(TestCase):

  def test_update_forward_split(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], None)
    sut = StockSplitAction(1, 3)
    sut.update(holding, portfolio)
    self.assertEqual(10/(3/1.0), holding.price)
    self.assertEqual(120*(3/1.0),  holding.shares)

  def test_update_reverse_split(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], None)
    sut = StockSplitAction(3, 1)
    sut.update(holding, portfolio)
    self.assertEqual(10/(1/3.0), holding.price)
    self.assertEqual(120*(1/3.0),  holding.shares)

class StockDividendActionTest(TestCase):

  def test_update(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], None)
    sut = StockDividendAction(1.075)
    sut.update(holding, portfolio)
    self.assertEqual(10/1.075, holding.price)
    self.assertEqual(120*1.075,  holding.shares)

class NameChangeActionTest(TestCase):

  def test_update(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], None)
    sut = NameChangeAction('Freemasons')
    sut.update(holding, portfolio)
    self.assertEqual('Freemasons', holding.description)

class SymbolChangeActionTest(TestCase):

  def test_update(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], None)
    sut = SymbolChangeAction('FM')
    sut.update(holding, portfolio)
    self.assertEqual('FM', holding.symbol)

class CurrencyConverterTest(TestCase):

  def test_convert_same(self):
    converter = CurrencyConverter()
    self.assertEqual(5.25*1.00, converter.convert(5.25, 'USD', 'USD'))

  def test_convert_different(self):
    converter = CurrencyConverter()
    self.assertEqual(5.25*1.32, converter.convert(5.25, 'USD', 'CAD'))

