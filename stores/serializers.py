from rest_framework import serializers

from payment.services import verify_payment_session
from .models import Category, Store
class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = ['id','shopname', 'description','phone','address','category','image_url' ]
    
    
class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']  

class StorePaidSerializer(serializers.ModelSerializer):
    verify_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Store
        fields = ['id', 'shopname', 'description', 'phone', 'address', 'category', 'image_url', 'verify_code']

    def create(self, validated_data):
        # Remove the 'verify_code' key from the validated_data
        verify_code = validated_data.pop('verify_code', None)
        request = self.context.get('request')
        # Do something with the 'verify_code' here, such as validation
        is_valid_payment = verify_payment_session(session_id=verify_code, user=request.user)

        if not is_valid_payment:
            raise serializers.ValidationError({"verify_code": "Payment session is invalid."}, code=402)

        # Create the store now that 'verify_code' is validated
        store = Store.objects.create(**validated_data)

        return store