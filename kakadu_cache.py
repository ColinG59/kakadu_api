from http.client import BAD_REQUEST
import requests
import random
import json
import threading
import time
import config

cache = []
api_key = config.API_TOKEN
api_url = config.API_URL

def get_cache():
    if cache:
        return cache
    else:
        return ["no content"]
    
def get_random_picture():
    
    anzahl = len(cache)
    randomzahl = random.randint(0, anzahl)
    print('RANDOMZAHL: ', randomzahl, anzahl)
    return cache[randomzahl]
    
def get_pictures():
    
    while True:
    
        api_request1 = requests.get(api_url+f'?key={api_key}&q=cockatoo&image_type=photo&lang=en&per_page=200&page=1')
        
        if not api_request1.status_code == 200: return
        
        api_response_dict1 = api_request1.json()
        picture_dict1 = api_response_dict1['hits']
        
        for pic in picture_dict1: add_to_cache(id=pic["id"], source_url=pic["pageURL"], type=pic["type"], url=pic["largeImageURL"])
        
        total_hits = int(api_response_dict1['totalHits'])
        
        if total_hits > 200:
            
            try:
                api_request2 = requests.get(api_url+f'?key={api_key}&q=cockatoo&image_type=photo&lang=en&per_page=200&page=2')
                if not api_request2.status_code == 200: raise BAD_REQUEST('bad request')
                api_response_dict2 = api_request2.json()
                picture_dict2 = api_response_dict2['hits']
                for pic in picture_dict2: add_to_cache(id=pic["id"], source_url=pic["pageURL"], type=pic["type"], url=pic["largeImageURL"])
            except:
                pass
            
            if total_hits > 400:
                
                try:
                    api_request3 = requests.get(api_url+f'?key={api_key}&q=cockatoo&image_type=photo&lang=en&per_page=200&page=3')
                    if not api_request3.status_code == 200: raise BAD_REQUEST('bad request')
                    api_response_dict3 = api_request3.json()
                    picture_dict3 = api_response_dict3["hits"]
                    for pic in picture_dict3: add_to_cache(id=pic["id"], source_url=pic["pageURL"], type=pic["type"], url=pic["largeImageURL"])
                except:
                    pass
        
        time.sleep(1*60*60)
        
    
def add_to_cache(id: str, source_url: str, type: str, url: str, weburl: str):
    data = {"id": id, "source_url": source_url, "type": type, "url": url, "web_url": weburl}
    if not id in cache:
        cache.append(data)
