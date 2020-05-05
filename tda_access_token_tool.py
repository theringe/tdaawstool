# -*- coding: UTF-8 -*-
from redis import *
import requests

r = Redis(host='127.0.0.1', port=6379, db=0)

response = requests.post(
    url='https://api.tdameritrade.com/v1/oauth2/token',
    data={
        'grant_type': 'refresh_token',
        'refresh_token': r.get('refresh_token').decode("utf-8"),
        'client_id': 'X@AMER.OAUTHAP' # please change X to your client_id you've gained from TD Ameritrade
    },
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })

r.setex('access_token', 1800, response.json()['access_token'])

response = requests.get(
    url='https://api.tdameritrade.com/v1/userprincipals?fields=streamerSubscriptionKeys,streamerConnectionInfo',
    headers={
        'Authorization': 'Bearer ' + r.get('access_token').decode("utf-8")
    })

r.setex('stream_token', 1800, response.text.replace('\n', '').replace(' ', ''))
