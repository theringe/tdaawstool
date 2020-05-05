# -*- coding: UTF-8 -*-
import websocket
from redis import *
import json
import time
from calendar import timegm
import calendar
from urllib.parse import urlencode
import boto3
from websocket_server import WebsocketServer
import asyncio
from concurrent.futures import ThreadPoolExecutor

# please specify the proper namespace you've gained from AWS
KINESIS_STREAM_NAME = 'XXXX'
REGION_NAME = 'XXXX'

def write_to_stream(event, region_name, stream_name):
    client = boto3.client('kinesis', region_name=region_name)
    res = client.put_record(
        StreamName=stream_name,
        Data=json.dumps(event) + '\n',
        PartitionKey=str(calendar.timegm(time.gmtime()))
    )
    return res


def message_received(c, s, message):
    s.send_message_to_all(message)
    ws.send(message)


def on_message(ws, message):
    if "response" in message:
        f = open("tda_streaming.log", "a+")
        f.write(message + '\n')
        f.close()

    if "data" in message:
        write_to_stream(message, REGION_NAME, KINESIS_STREAM_NAME)

    server.send_message_to_all(message)


def on_error(ws, error):
    f = open("tda_streaming.log", "a+")
    f.write(error + '\n')
    f.close()


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    data_symbol = json.loads(r.get('symbol').decode("utf-8").replace('\\"', '"'))
    symbol = data_symbol['SYMBOL']
    symbol_limit = data_symbol['SYMBOL_LIMIT']
    ws.send(json.dumps({
        "requests": [
            {
                "service": "ADMIN",
                "command": "LOGIN",
                "requestid": 1,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "credential": urlencode(credentials),
                    "token": stream_token['streamerInfo']['token'],
                    "version": "1.0"
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "ADMIN",
                "command": "QOS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "qoslevel": 0
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "QUOTE",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol),
                    "fields": ",".join([str(x) for x in range(0, 60)])
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "CHART_EQUITY",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol),
                    "fields": ",".join([str(x) for x in range(0, 10)])
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "NEWS_HEADLINE",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol),
                    "fields": ",".join([str(x) for x in range(0, 15)])
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "TIMESALE_EQUITY",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol),
                    "fields": ",".join([str(x) for x in range(0, 15)])
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "NASDAQ_BOOK",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol_limit),
                    "fields": ",".join([str(x) for x in range(0, 15)])
                }
            }
        ]
    }))
    time.sleep(2)
    ws.send(json.dumps({
        "requests": [
            {
                "service": "LISTED_BOOK",
                "command": "SUBS",
                "requestid": 2,
                "account": stream_token['accounts'][0]['accountId'],
                "source": stream_token['streamerInfo']['appId'],
                "parameters": {
                    "keys": ",".join(symbol_limit),
                    "fields": ",".join([str(x) for x in range(0, 15)])
                }
            }
        ]
    }))
    time.sleep(2)


async def ss(server):
    with ThreadPoolExecutor(max_workers=1) as executor:
        await loop.run_in_executor(executor, server.run_forever)


async def sc(ws):
    with ThreadPoolExecutor(max_workers=1) as executor:
        await loop.run_in_executor(executor, ws.run_forever)


if __name__ == '__main__':
    r = Redis(host='127.0.0.1', port=6379, db=0)

    stream_token = json.loads(r.get('stream_token').decode("utf-8").replace('\\"', '"'))
    credentials = {
        "userid": stream_token['accounts'][0]['accountId'],
        "token": stream_token['streamerInfo']['token'],
        "company": stream_token['accounts'][0]['company'],
        "segment": stream_token['accounts'][0]['segment'],
        "cddomain": stream_token['accounts'][0]['accountCdDomainId'],
        "usergroup": stream_token['streamerInfo']['userGroup'],
        "accesslevel": stream_token['streamerInfo']['accessLevel'],
        "authorized": "Y",
        "timestamp": timegm(
            time.strptime(stream_token['streamerInfo']['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S%z")) * 1000,
        "appid": stream_token['streamerInfo']['appId'],
        "acl": stream_token['streamerInfo']['acl']
    }

    server = WebsocketServer(9001)
    server.set_fn_message_received(message_received)

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://" + stream_token['streamerInfo']['streamerSocketUrl'] + "/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    loop = asyncio.get_event_loop()
    tasks = []
    tasks.append(loop.create_task(ss(server)))
    tasks.append(loop.create_task(sc(ws)))
    loop.run_until_complete(asyncio.wait(tasks))
