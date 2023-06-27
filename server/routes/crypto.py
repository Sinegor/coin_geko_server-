import json
import pydantic
import aiohttp
import requests
import asyncio

from server.routes._routers import crypto_router as c_router
from fastapi import APIRouter, Body, Request, HTTPException, Response
#from fastapi.encoders import jsonable_encoder
from fastapi import  status as response_status
from server.methods.request_methods import get_crypto_price, get_crypto_data, string_handling



@c_router.post("/currentprice")
async def get_priceies_from_coingeko(request:Request, crypto_list:list):        
        coin_geko_url = 'https://api.coingecko.com/api/v3/simple/price'
        crypto_list = [string_handling(asset) for asset in crypto_list]
        coin_geko_crud_data_task  = asyncio.create_task(get_crypto_price(coin_geko_url, crypto_list))
        crypto_data = await coin_geko_crud_data_task
        return  crypto_data
          
        
@c_router.post("/cryptodata")
async def get_data_from_coingeko(request:Request, crypto_list:list):
        """ В формате списка словарей получаем данные о текущей цене и циркулирующем предложении"""        
        coin_geko_url = 'https://api.coingecko.com/api/v3/coins/markets'
        crypto_list = [string_handling(asset) for asset in crypto_list]
        coin_geko_crud_data_task  = asyncio.create_task(get_crypto_data(coin_geko_url, crypto_list))
        crypto_data = await coin_geko_crud_data_task
        result_dict = {'checking_ids':[]}
        for coin in crypto_data:
                result_dict[coin['symbol']]={}
                result_dict[coin['symbol']]['price'], result_dict[coin['symbol']]['circulating_supply']= coin['current_price'],coin['circulating_supply']
                result_dict['checking_ids'].append(coin['id'])
        for request_coin in crypto_list:
                if request_coin not in result_dict['checking_ids']:
                        result_dict[request_coin] = "Такой монеты не существует, проверьте правильность написания"
        return  result_dict
    