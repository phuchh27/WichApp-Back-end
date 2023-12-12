import os
import redis
import json

from bill.models import Bill, BillDetail
from items.models import Item

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


def get_bills_and_profits_by_store_id(store_id):
    bills = Bill.objects.filter(store_id=store_id)
    bill_data = []

    for bill in bills:
        item_ids = BillDetail.objects.filter(bill_id=bill.id).values_list('product_id', flat=True)
        total_profit = 0

        for item_id in item_ids:
            quantity = BillDetail.objects.get(bill_id=bill.id, product_id=item_id).quantity
            cost, price = Item.objects.get(id=item_id).cost, Item.objects.get(id=item_id).price
            total_profit += (price - cost) * quantity

        bill_data.append({
            'bill_id': bill.id,
            'date_create': bill.date_create,
            'date_paid': bill.date_paid,
            'total_amount': bill.total_amount,
            'store_id': bill.store_id,
            'employee_name': bill.employee.username,  # Assuming User model has a 'username' field
            'total_profit': total_profit,
        })

    return bill_data