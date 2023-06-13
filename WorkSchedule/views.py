from datetime import datetime, timedelta
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.Repositories.Interfaces.IStaffRepository import OwnerRepository
from core.Repositories.Interfaces.IWorkScheduleRepository import WorkScheduleRepository
from core.Repositories.StaffRepository import OwnerRepositoryImpl
from core.Repositories.WorkScheduleReponsotory import WorkScheduleRepositoryImpl
from .serializers import (
    O_WorkScheduleSerializer,
    S_WorkScheduleSerializer,
    StaffWorkScheduleSerializer,
    WorkScheduleCreateSerializer,
    WorkScheduleSerializer,
)


### Owner ------------------------------------------
# -------------------------------------------- owner can create S_W for week --------------------------------------------
class WorkScheduleCreateView(generics.CreateAPIView):
    serializer_class = WorkScheduleCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def post(self, request, store_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        # Check if the current user is the owner of the store
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create the work schedules for the store
        schedule_repository.create_schedules_by_store_id(store_id)

        return Response(
            {"detail": "Work schedules created successfully."},
            status=status.HTTP_201_CREATED,
        )


work_schedule_create_view = WorkScheduleCreateView.as_view()


# -------------------------------------------- owner can view list S_W in store --------------------------------------------
class WorkScheduleListView(generics.ListAPIView):
    serializer_class = WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def get(self, request, store_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedules = schedule_repository.get_all_schedules_by_store_id(store_id)
        serializer = self.serializer_class(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


work_schedule_list_view = WorkScheduleListView.as_view()


# -------------------------------------------- owner can view detail S_W  --------------------------------------------
class WorkScheduleDetailView(generics.RetrieveAPIView):
    serializer_class = WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def get(self, request, store_id, schedule_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule = schedule_repository.get_detail_schedules_by_id(schedule_id, store_id)
        serializer = self.serializer_class(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)


work_schedule_detail_view = WorkScheduleDetailView.as_view()


# -------------------------------------------- view all day of week --------------------------------------------
class DaysOfWeekView(APIView):
    def get(self, request):
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=current_date.weekday())
        week_dates = []
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            week_dates.append(current_date.strftime("%d-%b-%Y"))

        return Response(week_dates, status=200)


# -------------------------------------------- owner can view all register of staff in week  --------------------------------------------
class OwnerWorkScheduleListView(generics.ListAPIView):
    serializer_class = StaffWorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def get(self, request, store_id, schedule_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedules = schedule_repository.get_all_schedule_for_staff(schedule_id)
        serializer = self.serializer_class(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


owner_work_schedule_list_view = OwnerWorkScheduleListView.as_view()


# -------------------------------------------- owner can <<CREATE>> Store S_W for week --------------------------------------------
class OwnerCreateWorkScheduleView(generics.CreateAPIView):
    serializer_class = O_WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def post(self, request, store_id, schedule_id, s_schedule_id):
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule_repository.create_schedule_of_owner(schedule_id, s_schedule_id)
        return Response(
            {"detail": "Work schedules created successfully."},
            status=status.HTTP_201_CREATED,
        )


owner_create_ws_f_week = OwnerCreateWorkScheduleView.as_view()


class OwnerDeleteWorkScheduleView(generics.DestroyAPIView):
    serializer_class = O_WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def delete(self, request, store_id,id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_owner_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule_repository.delete_schedule_of_owner(id)
        return Response({"detail": "Work schedules deleted successfully."}, status=status.HTTP_200_OK)
    
owner_delete_ws_f_week = OwnerDeleteWorkScheduleView.as_view()
### Staff ---------------------------------------------------


# -------------------------------------------- Staff <<CREATE>> register S-W  --------------------------------------------
class StaffCreateWorkScheduleView(generics.CreateAPIView):
    serializer_class = S_WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def post(self, request, store_id, schedule_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_staff_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule_repository.create_schedule_of_staff(
            schedule_id,
            serializer.validated_data,  # Access the validated data
            user_id,
        )
        return Response(
            {"detail": "Work schedules created successfully."},
            status=status.HTTP_201_CREATED,
        )


# -------------------------------------------- Staff can <<VIEW>> all S_W in week --------------------------------------------
class StaffWorkScheduleListView(generics.ListAPIView):
    serializer_class = StaffWorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()  # Replace with your actual implementation

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def get(self, request, store_id, schedule_id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_staff_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the staff of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedules = schedule_repository.get_all_schedule_for_staff(schedule_id)
        serializer = self.serializer_class(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


staff_work_schedule_list_view = StaffWorkScheduleListView.as_view()


# -------------------------------------------- owner can <<UPDATE>> S_W for week --------------------------------------------
class StaffWorkScheduleUpdateView(generics.UpdateAPIView):
    serializer_class = StaffWorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()  # Replace with your actual implementation

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def put(self, request, store_id, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_staff_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule_repository.update_schedule_of_staff(id, serializer.validated_data)
        return Response(
            {"detail": "Work schedules updated successfully."},
            status=status.HTTP_201_CREATED,
        )


staff_work_schedule_update_view = StaffWorkScheduleUpdateView.as_view()


# -------------------------------------------- owner can <<DELETE>> S_W for week --------------------------------------------
class StaffWorkScheduleDeleteView(generics.DestroyAPIView):
    serializer_class = StaffWorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_owner_repository(self):
        return OwnerRepositoryImpl()  # Replace with your actual implementation

    def get_schedule_repository(self):
        return WorkScheduleRepositoryImpl()

    def delete(self, request, store_id, id):
        owner_repository = self.get_owner_repository()
        schedule_repository = self.get_schedule_repository()
        user_id = request.user.id
        is_owner = owner_repository.is_staff_of_store(user_id, store_id)
        if not is_owner:
            return Response(
                {"detail": "You are not the owner of this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        schedule_repository.delete_schedule_of_staff(id)
        return Response(
            {"detail": "Work schedules deleted successfully."},
            status=status.HTTP_201_CREATED,
        )


staff_work_schedule_delete_view = StaffWorkScheduleDeleteView.as_view()
