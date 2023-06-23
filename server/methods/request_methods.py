import json
import aiohttp
import requests
import asyncio

from aiohttp import ClientSession

def sort_coin_data(d:dict):
    return d['name']

async def make_connection(session:ClientSession, url, params=None):
       async with session.get(url, params=params,) as response:
           if response.status == 429:
               time_delta = int(response.headers['Retry-After'])
               await asyncio.sleep(time_delta)
               repeat_request_task = asyncio.create_task(make_connection(session,url,params))
               return await repeat_request_task
           elif response.reason == 'Not Found':
               raise KeyError
           else:
                return await response.text()

def string_handling(str:str):
    return str.rstrip().lstrip().lower()


async def get_crypto_price(url, crypto_assets, fiat_coin='usd'):
    try:
        connector = aiohttp.TCPConnector(limit=50, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            params_query = {
            'ids': ','.join(crypto_assets),
            'vs_currencies': fiat_coin
            }
            response_data_task = asyncio.create_task(make_connection(session, url, params_query))
            response_data = await response_data_task
            data_dict = json.loads(response_data)
            result_data = {}
            for crypto in crypto_assets:
                result_data[crypto]= data_dict[crypto][fiat_coin] 
            return result_data 
    except KeyError as e:
        result_data[crypto] = 'Такой монеты не существует, проверьте правильность написания'
        return result_data 

async def get_crypto_data(url, crypto_assets, fiat_coin='usd'):
            connector = aiohttp.TCPConnector(limit=50, force_close=True)
            async with aiohttp.ClientSession(connector=connector) as session:
                params_query = {
                'ids': ','.join(crypto_assets),
                'vs_currency': fiat_coin
                }
                response_data_task = asyncio.create_task(make_connection(session, url, params_query))
                response_data = await response_data_task
                result_data = json.loads(response_data)
                result_data.sort(key= sort_coin_data)
                return result_data
        