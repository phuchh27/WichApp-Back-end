from datetime import timezone
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView

from bill.services import delete_bill_data_from_redis, delete_bill_details_data_from_redis, get_bill_data_from_redis, get_bill_details_data_from_redis

from .models import Bill
from .serializers import  BillPaySerializer, BillSerializer, BillUpdateSerializer

from authentication import services

import redis
import json


class BillCreateAPIView(generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'status': 'error', 'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        current_user = self.request.user.id
        employee_id = request.data.get('employee_id', None)
        isStaff = services.is_user_staff(current_user)
        get_store = services.get_store_id_by_user(current_user)

        if not isStaff:
            return Response({'status': 'error', 'message': 'User is not a staff member'}, status=status.HTTP_403_FORBIDDEN)
        if get_store is None:
            return Response({'status': 'error', 'message': 'User is not associated with a store'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if employee_id:
            serializer.save(employee_id=employee_id, store_id=get_store)
        else:
            serializer.save(employee_id=current_user, store_id=get_store)

        return Response({'status': 'success', 'bill_data': serializer.data}, status=status.HTTP_201_CREATED)


class BillListByStoreId(APIView):
    
    def get(self, request, *args, **kwargs):

        current_user = self.request.user.id
        user_store_id = services.get_store_id_by_user(current_user)

        redis_client = redis.Redis()
        all_keys = redis_client.keys("bill:*")

        # 3. Lọc ra các keys phù hợp với store_id
        matching_keys = [key.decode(
            "utf-8") for key in all_keys if f'StoreId_{user_store_id}' in key.decode("utf-8")]
        print(matching_keys)
        # 4. Lấy dữ liệu từ Redis cho những keys quan tâm
        bills = []
        for key in matching_keys:
            bill_json = redis_client.get(key)
            if bill_json is not None:
                id_part = key.split(':')[1]
                bill = json.loads(bill_json)
                bill['id'] = id_part
                bills.append(bill)
        # 5. Trả về dữ liệu dưới dạng JSON
        return Response(bills, status=status.HTTP_200_OK)


class BillDetailAPIView(APIView):
    def get(self, request, key, format=None):
        redis_client = redis.Redis()

        # Construct the Redis key based on the received key
        redis_key = f'bill_detail:{key}'

        # Retrieve data from Redis
        bill_detail_json = redis_client.get(redis_key)

        if bill_detail_json is not None:
            # Parse the JSON data
            bill_detail = json.loads(bill_detail_json)
            return Response(bill_detail, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Bill detail not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateBillView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BillUpdateSerializer(data=request.data)

        if serializer.is_valid():
            bill_id = serializer.validated_data['bill_id']
            billEditing = serializer.validated_data['billEditing']
            billtotal = serializer.validated_data['billtotal']

            redis_instance = redis.StrictRedis(
                host='localhost', port=6379, db=0)

            # Retrieve existing bill_detail from Redis
            existing_bill_detail = redis_instance.get(f'bill_detail:{bill_id}')

            if existing_bill_detail:
                existing_bill_detail = json.loads(
                    existing_bill_detail.decode('utf-8'))

                # Update the existing bill_detail in Redis
                redis_instance.set(
                    f'bill_detail:{bill_id}', json.dumps(billEditing))

                # Update total_amount in Redis
                existing_data = redis_instance.get(f'bill:{bill_id}')
                if existing_data:
                    existing_data = json.loads(existing_data.decode('utf-8'))
                    existing_data['total_amount'] = str(billtotal)
                    redis_instance.set(
                        f'bill:{bill_id}', json.dumps(existing_data))

                return Response({"message": "Bill updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Bill not found in Redis"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBillView(APIView):
    def delete(self, request, bill_id, *args, **kwargs):
        try:

            redis_instance = redis.StrictRedis(
                host='localhost', port=6379, db=0)
            redis_instance.delete(f'bill_detail:{bill_id}')
            redis_instance.delete(f'bill:{bill_id}')

            return Response({"message": "Bill deleted successfully"}, status=status.HTTP_200_OK)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)


class PayBillView(APIView):
    def post(self, request, *args, **kwargs):
        bill_data = get_bill_data_from_redis(request.data['bill_id'])
        bill_details_data = get_bill_details_data_from_redis(request.data['bill_id'])

        employee_id = bill_data.get('employee_id', '')
        employee_id_parts = employee_id.split('_')
        extracted_employee_id = employee_id_parts[0] if employee_id_parts else None

        bill_data['employee_id'] = extracted_employee_id

        modified_bill_details_data = []
        for bill_detail in bill_details_data:
            product_data = bill_detail.get('product', {})
            if not product_data:
                return Response({"bill_details": [{"product": ["This field is required."]}]}, status=status.HTTP_400_BAD_REQUEST)

            product_id = product_data.get('id', None)
            modified_bill_detail = {
                'product_id': product_id,  
                'quantity': bill_detail.get('quantity', 0),
            }
            modified_bill_details_data.append(modified_bill_detail)

        serializer = BillPaySerializer(data={**bill_data, 'bill_details': modified_bill_details_data})
        if serializer.is_valid():
            serializer.save()
            
            delete_bill_data_from_redis(request.data['bill_id'])
            delete_bill_details_data_from_redis(request.data['bill_id'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







