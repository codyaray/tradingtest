#!/usr/bin/env python
"""
Simple tool to check whether the network port follows our port numbering standard for each exchange.
"""
def calculate_port(ip):
  w, x, y, z = ip.split('.')
  return 50000 + 200 * int(y) + int(z)


def extract_address_and_port(filename):
  lines = [line.rstrip() for line in open(filename).readlines()]
  for line in lines:
    details = line.split('=')[1]
    actual_port, ip = details.split(' ')[0:2]
    yield ip[1:], int(actual_port)


def main(filename):
  for ip, actual_port in extract_address_and_port(filename):
    expected_port = calculate_port(ip)
    if actual_port != expected_port:
      print "%s expected %s, found %s" % (ip, expected_port, actual_port)

if __name__ == '__main__':
  main('fileC.txt')
