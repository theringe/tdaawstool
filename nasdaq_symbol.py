# -*- coding: UTF-8 -*-
from redis import *
import json
import requests

r = Redis(host='127.0.0.1', port=6379, db=0)

response = requests.get(
    'https://www.nasdaq.com/api/v1/screener?sector=Technology&marketCap=Mega,Large&page=1&pageSize=1000')
data_nasdaq = response.json()
symbol_nasdaq = []
for x in data_nasdaq['data']:
    symbol_nasdaq.append(x['ticker'])

response = requests.get(
    'https://www.nasdaq.com/api/v1/screener?sector=Technology&marketCap=Mega,Large&analystConsensus=StrongBuy,StrongSell&page=1&pageSize=1000')
data_limit_nasdaq = response.json()
symbol_limit_nasdaq = []
for x in data_limit_nasdaq['data']:
    symbol_limit_nasdaq.append(x['ticker'])

with open('symbol.json') as symbol_file:
    data_local = json.load(symbol_file)
    symbol_local = data_local['SYMBOL']
    symbol_limit_local = data_local['SYMBOL_LIMIT']

symbol = list(set(symbol_nasdaq) | set(symbol_local))
symbol.sort()
symbol_limit = list(set(symbol_limit_nasdaq) | set(symbol_limit_local))
symbol_limit.sort()

if len(symbol) > 1000:
    symbol = symbol_local
if len(symbol_limit) > 100:
    symbol_limit = symbol_limit_local

f = open("symbol.json", "w+")
f.write(json.dumps({
    'SYMBOL': symbol,
    'SYMBOL_LIMIT': symbol_limit
}))
f.close()

r.set('symbol', json.dumps({
    'SYMBOL': symbol,
    'SYMBOL_LIMIT': symbol_limit
}))
