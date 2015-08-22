#!/usr/bin/env python
"""
Simulates actions taken on a corporate portfolio. Prints the resulting
portfolio after each simulated day's actions are complete.

Usage: ./problem3.py [portfolio-file] [actions-file]

Positional Arguments:
  portfolio-file FILENAME  defaults to 'portfolio.csv'
  actions-file FILENAME  defaults to 'corporate_actions.csv'

See the committed files for format examples.
"""
from argparse import ArgumentParser, FileType
from locale import setlocale, LC_ALL

from problem3.actions import CurrencyConverter
from problem3.serializers import CsvPortfolioSerializer, CsvActionsSerializer, ActionParser

setlocale(LC_ALL, 'en_US.UTF-8')


class ActionsSimulator(object):

  def __init__(self, parser):
    self.parser = parser

  def apply(self, action, portfolio):
    self.parser.parse(action.description).update(portfolio.holdings[action.symbol], portfolio)


def main(portfolio_file, actions_file, reinvest_dividends):
  serializer = CsvPortfolioSerializer
  converter = CurrencyConverter()
  portfolio = serializer.deserialize(portfolio_file, converter, reinvest_dividends)
  actions = CsvActionsSerializer.deserialize(actions_file)
  simulator = ActionsSimulator(ActionParser())

  print "Initial Portfolio"
  print serializer.serialize(portfolio).getvalue()

  current_date = None
  for action in actions:
    simulator.apply(action, portfolio)

    if not current_date or current_date != action.date:
      print "Portfolio after %s" % action.date
      print serializer.serialize(portfolio).getvalue()
      current_date = action.date

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--portfolio', dest='portfolio_file', help="Portfolio CSV filename", default='portfolio.csv', type=FileType('r'))
  parser.add_argument('--actions', dest='actions_file', help="Actions CSV filename", default='corporate_actions.csv', type=FileType('r'))
  parser.add_argument('-r', '--reinvest-dividends', help="Simulate with reinvested dividends", action='store_true')
  args = parser.parse_args()

  main(args.portfolio_file, args.actions_file, args.reinvest_dividends)
