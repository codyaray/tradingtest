from unittest import TestCase
from problem3.actions import CurrencyConverter
from problem3.models import Holding, Portfolio


class PortfolioTest(TestCase):

  CONVERTER = CurrencyConverter()

  def test_value_one_holding(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    portfolio = Portfolio([holding], self.CONVERTER)
    self.assertEqual(1200, portfolio.value())

  def test_value_two_holdings(self):
    holdings = [
      Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD'),
      Holding('FM', 'Freemasons', 'US', 250, 25, 'USD')
    ]
    portfolio = Portfolio(holdings, self.CONVERTER)
    self.assertEqual(7450, portfolio.value())

  def test_value_two_holdings_with_cash(self):
    holdings = [
      Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD'),
      Holding('FM', 'Freemasons', 'US', 250, 25, 'USD')
    ]
    portfolio = Portfolio(holdings, self.CONVERTER)
    portfolio.cash_value = 550
    self.assertEqual(8000, portfolio.value())

  def test_value_another_currency(self):
    holdings = [
      Holding('IL', 'Illuminati', 'BY', 120, 10, 'CAD'),
      Holding('FM', 'Freemasons', 'US', 250, 25, 'USD')
    ]
    portfolio = Portfolio(holdings, self.CONVERTER)
    portfolio.cash_value = 550
    share_price = 10 * self.CONVERTER.CONVERSION_TABLE[('CAD', 'USD')]
    self.assertEqual(120*share_price + 250*25 + 550, portfolio.value())

class HoldingTest(TestCase):

  def test_total_value(self):
    holding = Holding('IL', 'Illuminati', 'BY', 120, 10, 'USD')
    self.assertEqual(1200, holding.total_value())
