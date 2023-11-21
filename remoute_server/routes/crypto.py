import json
import pydantic
import aiohttp
import requests
import asyncio
import os


from dotenv import load_dotenv
from remoute_server.routes._routers  import crypto_router as c_router
from fastapi import APIRouter, Body, Request, HTTPException, Response
from fastapi import  status as response_status
from remoute_server.methods.request_methods import get_crypto_price, get_crypto_data, string_handling, get_data_market_from_coingeko
from remoute_server.methods.data_workong_methods import get_data_from_file, get_data_of_coin, extract_item_from_market_data
load_dotenv()
path = os.getenv('PATH_TO_LIST_COINS')


@c_router.post("/cryptodata/coin_geko_market_data")
async def get_data_from_coingeko(request:Request, crypto_data:dict):
        """ The function receives the dict whith two property: coinsIds - list of the coins id and requiredProperties - list of the
        properties, which nessesary send client. CoinsIds sends to the Coin Geko API. 
        Возвращает словарь, в котормо айдишник является словарём, а свойствами содержимое requiredProperties
        """        
        crypto_list = await get_data_market_from_coingeko (crypto_data['coinsIds'])
#         result_dict = {} 
# #Checking_ids include coins for which information is obtained from the Coin Geko API. 
# # If there is no coin, in particular if it is misspelled, the API does not return an explicit error. 
# # This list is necessary to inform the user on which coins the data is not received. 
# # Temporary solution, you need to redo.
#         for coin in crypto_data:
#                 result_dict[coin['id']]={}
#                 result_dict[coin['id']]['price'], result_dict[coin['id']]['circulating_supply']= coin['current_price'],coin['circulating_supply']
#         return  result_dict
        result = extract_item_from_market_data(crypto_list, crypto_data['coinsIds'], *crypto_data['requiredProperties'] )
        return result


@c_router.post("/convert_data")
async def convert_data_to_coingeko_id(request:Request, data_list:dict):
        """Принимает данные в формате словаря тремя свойствами: oldId, newId, dataOfOldId (первые два названия параметров, третий массив со значемнями старого айди)
           Возращает данные в формате {{oldId}:{'newId':item}}
        """
        coin_list = get_data_from_file(path)
        result_data = get_data_of_coin(coin_list, data_list)
        return result_data

