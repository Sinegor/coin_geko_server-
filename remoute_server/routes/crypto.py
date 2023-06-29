import json
import pydantic
import aiohttp
import requests
import asyncio

from remoute_server.routes._routers  import crypto_router as c_router
from fastapi import APIRouter, Body, Request, HTTPException, Response
from fastapi import  status as response_status
from remoute_server.methods.request_methods import get_crypto_price, get_crypto_data, string_handling


        
@c_router.post("/cryptodata")
async def get_data_from_coingeko(request:Request, crypto_list:list):
        """ The function receives the list of coins and sends them to the Coin Geko API. From the response, 
        Google sheets provides information about the current price and the circulating offer of each coin."""        
        coin_geko_url = 'https://api.coingecko.com/api/v3/coins/markets'
        crypto_list = [string_handling(asset) for asset in crypto_list]
        coin_geko_crud_data_task  = asyncio.create_task(get_crypto_data(coin_geko_url, crypto_list))
        crypto_data = await coin_geko_crud_data_task
        result_dict = {'checking_ids':[]} 
#Checking_ids include coins for which information is obtained from the Coin Geko API. 
# If there is no coin, in particular if it is misspelled, the API does not return an explicit error. 
# This list is necessary to inform the user on which coins the data is not received. 
# Temporary solution, you need to redo.
        for coin in crypto_data:
                result_dict[coin['symbol']]={}
                result_dict[coin['symbol']]['price'], result_dict[coin['symbol']]['circulating_supply']= coin['current_price'],coin['circulating_supply']
                result_dict['checking_ids'].append(coin['id'])
        for request_coin in crypto_list:
                if request_coin not in result_dict['checking_ids']:
                        result_dict[request_coin] = "There is no such coin, check the spelling correctly"
        return  result_dict
    