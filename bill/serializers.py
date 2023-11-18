from decimal import Decimal
import json

import redis
from items.models import Item
from .models import Bill, BillDetail, generate_random_id

from rest_framework import serializers

from authentication import services

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'price')
        ref_name = 'BillItem'

class BillDetailSerializer(serializers.ModelSerializer):
    product = ItemSerializer()
    class Meta:
        model = BillDetail
        fields = ('product', 'quantity')   

class BillSerializer(serializers.ModelSerializer):
    bill_details = BillDetailSerializer(many=True, write_only=True)

    class Meta:
        model = Bill
        fields = ('store_id', 'total_amount', 'bill_details')

    
    def create(self, validated_data):
        bill_details_data = validated_data.pop('bill_details', [])

        # Create Bill instance without saving to the database
        bill = Bill(**validated_data)

        # Save Bill to Redis
        json_string = json.dumps(validated_data, cls=DecimalEncoder)
        redis_client = redis.Redis()
        redis_client.set(f'bill:{bill.id}_StoreId_{bill.store.id}', json_string)

        # Create BillDetail instances and save to Redis
        detail_list = []
        for detail_data in bill_details_data:
            product_data = detail_data['product']
            product = Item.objects.get(id=product_data['id'])
            quantity = detail_data['quantity']

            # Create BillDetail instance without saving to the database
            bill_detail = BillDetail(bill=bill, product=product, quantity=quantity)

            detail_list.append({
                'product': ItemSerializer(product).data,
                'quantity': quantity,
            })

        detail_json_string = json.dumps(detail_list, cls=DecimalEncoder)
        redis_client.set(f'bill_detail:{bill.id}_StoreId_{bill.store.id}', detail_json_string)

        return bill

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class CartItemSerializer(serializers.Serializer):
    product = serializers.DictField()
    quantity = serializers.IntegerField()

class BillUpdateSerializer(serializers.Serializer):
    bill_id = serializers.CharField()
    billEditing = CartItemSerializer(many=True)
    billtotal = serializers.FloatField()



class BillDetailForPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = ['product', 'quantity']

class BillForPaySerializer(serializers.ModelSerializer):
    bill_details = BillDetailSerializer(many=True)

    class Meta:
        model = Bill
        fields = ['id', 'date_create', 'date_paid', 'total_amount', 'store', 'employee', 'bill_details']