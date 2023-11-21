import json

from remoute_server.methods.request_methods import string_handling


def get_data_from_file(path_to_file):
    with open(path_to_file) as my_file:
        crud_data = my_file.read()
        data_list = json.loads(crud_data)
        return data_list

def get_data_of_coin (banchmark_data:list, client_data:dict):
        result_data = {}
        for coin in client_data['dataOfOldId']:
            for item in banchmark_data:
                oldIdValue = string_handling(coin)
                result_data[coin] ={}
                if oldIdValue != string_handling(item[client_data['oldId']]):
                        result_data[coin]['newItem']  = f"не найдено, проверьте правильность заполнения графы {client_data['oldId']}"
                        continue
                else:
                        result_data[coin]['newItem'] = item[client_data['newId']]
                        break
        return result_data

def extract_item_from_market_data(market_data:list, request_coins:list, *items):
        result_dict = {} 
        """ 
        Function returns dict, where keys is id of coins, recieved from CoinGeko. Properties of this keys  are dict and content 
        of items. If required coin dont finded in CoinGeko, id of this coin - are key of the dict, but value of this key is not dict, info string   
        """
        for coin in market_data:
                result_dict[coin['id']]={}
                for item in items:
                        result_dict[coin['id']][item] = coin[item]
                request_coins.remove(coin['id'])
        if len(request_coins)!=0:
              for coin in request_coins:
                    result_dict[coin] = 'Такая монета не найдена, проверьте правильность заполнения графы id'                
        return  result_dict





    
        
