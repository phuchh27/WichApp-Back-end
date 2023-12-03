import os
import redis
import json

REDIS_URL = "redis://red-clfc6rmf27hc739blpi0:6379"


def get_bill_data_from_redis(bill_id):
    redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
    bill_data_json = redis_instance.get(f'bill:{bill_id}')

    if bill_data_json:
        return json.loads(bill_data_json.decode('utf-8'))
    else:
        return None

def get_bill_details_data_from_redis(bill_id):
    
    redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
    bill_details_data_json = redis_instance.get(f'bill_detail:{bill_id}')

    if bill_details_data_json:
        return json.loads(bill_details_data_json.decode('utf-8'))
    else:
        return None
    
def delete_bill_data_from_redis(bill_id):
    redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_instance.delete(f'bill:{bill_id}')

def delete_bill_details_data_from_redis(bill_id):
    redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_instance.delete(f'bill_detail:{bill_id}')
