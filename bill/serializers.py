from items.models import Item
from .models import Bill, BillDetail

from rest_framework import serializers

from authentication import services


class BillDetailSerializer(serializers.ModelSerializer):
    
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

        # Create Bill instance without details
        bill_instance = Bill.objects.create(**validated_data)

        for detail_data in bill_details_data:
            product = detail_data['product']
            quantity = detail_data['quantity']

            if product.quantity < quantity:
                raise serializers.ValidationError(f"Just have {product.quantity} Product {product.name} in the store is not enough quantity to sell..")

        # Create Bill instance without details
        bill_instance = Bill.objects.create(**validated_data)

        for detail_data in bill_details_data:
            product = detail_data['product']
            quantity = detail_data['quantity']

            product.quantity -= quantity
            product.save()

            # Create BillDetail instance
            BillDetail.objects.create(bill=bill_instance, product=product, quantity=quantity)

        return bill_instance






