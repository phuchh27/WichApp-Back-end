from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Bill
from .serializers import BillSerializer

from authentication import services

class BillCreateAPIView(generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'status': 'error', 'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        curent_user = self.request.user.id
        isStaff = services.is_user_staff(curent_user)
        get_store  = services.get_store_id_by_user(curent_user)

        if not isStaff:
            return Response({'status': 'error', 'message': 'User is not a staff member'}, status=status.HTTP_403_FORBIDDEN)
        if get_store is None:
            return Response({'status': 'error', 'message': 'User is not associated with a store'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['store_id'] = get_store
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'status': 'success', 'bill_data': serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        curent_user = self.request.user.id
        get_store  = services.get_store_id_by_user(curent_user)
        serializer.save(employee_id=curent_user,store_id = get_store)
