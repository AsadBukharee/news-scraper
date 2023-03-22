import ast
import json

from redis.client import Redis
redis_client = Redis(host='127.0.0.1', port=6379, db=0)


def get_news_redis(lates = True,website='elaosboa'):
    try:


        news_keys = redis_client.get('news_keys')
        if news_keys:
            news_keys = ast.literal_eval(news_keys.decode())
        if lates:
            news_keys = [news_keys[-1]]

        for key in news_keys:
            # news_doc = redis_client.get(f'{key}')
            with open(f'news_jsons/{key}/data.json', "r") as file:
                data = json.load(file)
                # if news_doc:
                #     news_doc = news_doc.decode('utf-8').replace("\'",'"')
                #     print(news_doc)
                return {"status": "true", "message": data}
        return {"status": "false", "message": f"Data expired, rescrap {website}"}
    except Exception as e:
        return {"status":"false","message":f"{e}"}


def get_title_redis(lates = True):
    try:


        news_keys = redis_client.get('news_keys')
        if news_keys:
            news_keys = ast.literal_eval(news_keys.decode())
        if lates:
            news_keys = [news_keys[-1]]

        for key in news_keys:
            # news_doc = redis_client.get(f'{key}')
            with open(f'news_jsons/{key}/titles.json', "r") as file:
                data = json.load(file)
                # if news_doc:
                #     news_doc = news_doc.decode('utf-8').replace("\'",'"')
                #     print(news_doc)
                return {"status": "true", "message": data}
        return {"status": "false", "message": f"Data expired, rescrap {website}"}
    except Exception as e:
        return {"status":"false","message":f"{e}"}