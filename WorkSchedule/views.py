from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.Repositories.Interfaces.IStaffRepository import OwnerRepository
from core.Repositories.Interfaces.IWorkScheduleRepository import WorkScheduleRepository
from core.Repositories.StaffRepository import OwnerRepositoryImpl
from core.Repositories.WorkScheduleReponsotory import WorkScheduleRepositoryImpl
from .serializers import WorkScheduleCreateSerializer

class WorkScheduleCreateView(generics.CreateAPIView):
    serializer_class = WorkScheduleCreateSerializer
    permission_classes = [IsAuthenticated]
    def get_owner_repository(self):
        return OwnerRepositoryImpl()  # Replace with your actual implementation

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()
    
    # def __init__(self, *args, **kwargs):
    #     self.owner_repository = kwargs.pop('owner_repository', None)
    #     self.schedule_repository = kwargs.pop('schedule_repository', None)
    #     super().__init__(*args, **kwargs)

    def post(self, request, store_id):
        
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        # Check if the current user is the owner of the store
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response({"detail": "You are not the owner of this store."},
                            status=status.HTTP_403_FORBIDDEN)

        # Create the work schedules for the store
        schedule_repository.create_schedules_by_store_id(store_id)

        return Response({"detail": "Work schedules created successfully."},
                        status=status.HTTP_201_CREATED)

work_schedule_create_view = WorkScheduleCreateView.as_view()

class WorkScheduleListView(generics.ListAPIView):
    serializer_class = WorkScheduleCreateSerializer
    permission_classes = [IsAuthenticated]
    def get_owner_repository(self):
        return OwnerRepositoryImpl()  # Replace with your actual implementation

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()
    def get (self, request, store_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response({"detail": "You are not the owner of this store."},
                            status=status.HTTP_403_FORBIDDEN)
        schedules  = schedule_repository.get_all_schedules_by_store_id(store_id)
        serializer = self.serializer_class(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
work_schedule_list_view = WorkScheduleListView.as_view()