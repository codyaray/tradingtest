from unittest import TestCase
from problem3.actions import CashDividendAction, StockSplitAction, StockDividendAction, SymbolChangeAction, NameChangeAction
from problem3.serializers import ActionParser


class ActionParserTest(TestCase):

  def test_parse_dividend(self):
    self.assertEqual(CashDividendAction(0.02, 'USD'), ActionParser.parse("Cash dividend - 0.02 USD/share"))

  def test_parse_stock_split(self):
    self.assertEqual(StockSplitAction(10, 9), ActionParser.parse("Stock split - 9 for 10"))

  def test_parse_stock_dividend(self):
    self.assertEqual(StockDividendAction(1.075), ActionParser.parse("Stock dividend - 1.075/share"))

  def test_parse_symbol_change(self):
    self.assertEqual(SymbolChangeAction('BB'), ActionParser.parse("Symbol change - new symbol is BB"))

  def test_parse_name_change(self):
    self.assertEqual(NameChangeAction('Blackberry'), ActionParser.parse("Name change - new name is \"Blackberry\""))
