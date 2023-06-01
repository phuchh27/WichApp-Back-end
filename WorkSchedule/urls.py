from django.urls import path

from WorkSchedule.views import work_schedule_create_view,work_schedule_list_view

urlpatterns = [
    path("<int:store_id>/work-schedules/", work_schedule_create_view, name="work-schedule"),
    path("<int:store_id>/work-schedule-list/", work_schedule_list_view, name="work-schedule-list"),
]
