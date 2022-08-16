import numpy as np
from datetime import datetime
from dateutil import tz
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import requests
import base64
import ast
import os

# times for time conversion
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
# ------------------------------------------------------------ #
ppm_limit = .08
ash_ppm_limit = 15
merge_limit = 3

url = "https://api.opensea.io/api/v1/events"

# merge contract address
contract = "0xc3f8a0F5841aBFf777d3eefA5047e8D413a1C9AB"

# opensea api key goes in 'header'
opensea_api_key = os.environ['OPENSEA_API_KEY']
headers = {"X-API-KEY": opensea_api_key}

# You need occured_before and catch created_date from response json

for i in range(0, 2):
    # querystring = {"asset_contract_address": contract, 
    #                "event_type": "created",
    #                "only_opensea": "true",
    #                "offset":i*50,
    #                "limit":"50"}
    querystring = {"asset_contract_address": contract, 
                   "event_type": "created",
                   "only_opensea": "true"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    sale_events = response.json()['asset_events']
    Nevents = len(sale_events)

    for j in range(Nevents):
        # avoid bundles
        if int(sale_events[j]['quantity']) == 1:
            list_time_utc = sale_events[j]['created_date']
            utc = datetime.strptime(list_time_utc.replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S')
            utc = utc.replace(tzinfo = from_zone)
            local_tx_time = utc.astimezone(to_zone)
            if sale_events[j]['payment_token']['symbol'] == 'ETH':
                dprice = sale_events[j]['starting_price']
                decimals = sale_events[j]['payment_token']['decimals']
                price_symbol = sale_events[j]['payment_token']['symbol']
                price = float(dprice) / 10**(decimals)
                token_ID = sale_events[j]['asset']['token_id']

                metadata = ast.literal_eval(base64.b64decode(sale_events[j]['asset']['token_metadata'].split(',')[-1]).decode("utf-8"))
                attributes = metadata['attributes']

                for j1 in range(len(attributes)):
                    if attributes[j1]['trait_type'] == 'Mass':
                        Mass = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Tier':
                        Tier = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Class':
                        mClass = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Merges':
                        Merges = attributes[j1]['value']

                ppm = price / float(Mass)

                if ppm <= ppm_limit:

                    print('--------------------------')
                    print('Token ID: ', token_ID)
                    print('Mass: ', Mass)
                    print('Tier: ', Tier)
                    print('Class: ', mClass)
                    print('Merges: ', Merges)
                    print('Price: ', price)
                    print('Price per mass: ', ppm)
                    print('Time: ', local_tx_time)

                if Tier >= 2:

                    print('--------------------------')
                    print('------ Higher Tier -------')
                    print('Token ID: ', token_ID)
                    print('Mass: ', Mass)
                    print('Tier: ', Tier)
                    print('Class: ', mClass)
                    print('Merges: ', Merges)
                    print('Price: ', price)
                    print('Price per mass: ', ppm)
                    print('Time: ', local_tx_time)

                if Merges >= merge_limit:

                    print('--------------------------')
                    print('------ High Merges -------')
                    print('Token ID: ', token_ID)
                    print('Mass: ', Mass)
                    print('Tier: ', Tier)
                    print('Class: ', mClass)
                    print('Merges: ', Merges)
                    print('Price: ', price)
                    print('Price per mass: ', ppm)
                    print('Time: ', local_tx_time)

            elif sale_events[j]['payment_token']['symbol'] == 'ASH':
                dprice = sale_events[j]['starting_price']
                decimals = sale_events[j]['payment_token']['decimals']
                price_symbol = sale_events[j]['payment_token']['symbol']
                price = float(dprice) / 10**(decimals)
                token_ID = sale_events[j]['asset']['token_id']

                metadata = ast.literal_eval(base64.b64decode(sale_events[j]['asset']['token_metadata'].split(',')[-1]).decode("utf-8"))
                attributes = metadata['attributes']

                for j1 in range(len(attributes)):
                    if attributes[j1]['trait_type'] == 'Mass':
                        Mass = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Tier':
                        Tier = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Class':
                        mClass = attributes[j1]['value']
                    if attributes[j1]['trait_type'] == 'Merges':
                        Merges = attributes[j1]['value']

                ppm = price / float(Mass)

                if ppm <= ash_ppm_limit:

                    print('--------------------------')
                    print('---------- ASH -----------')
                    print('Token ID: ', token_ID)
                    print('Mass: ', Mass)
                    print('Tier: ', Tier)
                    print('Class: ', mClass)
                    print('Merges: ', Merges)
                    print('Price: ', price)
                    print('Price per mass: ', ppm)
                    print('Time: ', local_tx_time)

                if Tier >= 2:

                    print('--------------------------')
                    print('---- ASH Higher Tier -----')
                    print('Token ID: ', token_ID)
                    print('Mass: ', Mass)
                    print('Tier: ', Tier)
                    print('Class: ', mClass)
                    print('Merges: ', Merges)
                    print('Price: ', price)
                    print('Price per mass: ', ppm)
                    print('Time: ', local_tx_time)



