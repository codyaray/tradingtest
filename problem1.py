#!/usr/bin/env python
"""
Given a list of symbols and gateway risks, determines which symbols are not
found in the gateway risks for exchangeB-groupA and exchangeC-groupA.
"""

def main(symbols, exchanges):
  """
  Finds all symbols which are not in exchangeB-groupA or in exchangeC-groupA
  """
  gateway_risks = parse_exchanges(exchanges)
  for symbol in symbols:
    if symbol not in gateway_risks[('exchangeB', 'groupA')] and \
        symbol not in gateway_risks[('exchangeC', 'groupA')]:
      print symbol

def parse_exchanges(exchanges):
  """
  Return the gateway_risks grouped by (exchange_id, group_id) and then grouped by symbol.

  For example, gateway_risk[(exchange, group)][symbol] => [risk1, risk2]
  """
  gateway_risks = {}
  for exchange in exchanges:
    columns = exchange.replace('=', ' = ').split(' ')
    exchange, group = columns[0].split('.')[0].split('_')
    risks = columns[2:]
    symbols_risk = {risks[x]: risks[x+1:x+3] for x in xrange(0, len(risks), 3)}
    gateway_risks[(exchange, group)] = symbols_risk
  return gateway_risks

if __name__ == '__main__':
  symbols = [line.rstrip() for line in open('fileA.txt').readlines()]
  exchanges = [line.rstrip() for line in open('fileB.txt').readlines()]
  main(symbols, exchanges)
