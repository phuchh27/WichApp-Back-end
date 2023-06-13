from WorkSchedule.models import O_WorkSchedule, WorkSchedule, S_WorkSchedule
from core.Repositories.Interfaces.IWorkScheduleRepository import WorkScheduleRepository
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from calendar import month_name
from typing import List
from authentication.models import User


class WorkScheduleRepositoryImpl(WorkScheduleRepository):
    def create_schedules_by_store_id(self, store_id: int) -> None:
        # Get the current month and week number
        current_date = datetime.now()
        month = current_date.strftime("%B")
        week = (current_date.day - 1) // 7 + 1
        # Calculate the start and closing dates
        start_day = current_date.date()
        closing_date = start_day + timedelta(days=7)
        title = f"Register work for {month} - Week {week}"
        description = f"{start_day} to {closing_date}"

        # Create the work schedule
        work_schedule = WorkSchedule.objects.create(
            title=title,
            description=description,
            start_day=start_day,
            closing_date=closing_date,
            store_id=store_id,
        )
        return work_schedule

    def get_all_schedules_by_store_id(self, store_id: int) -> List[WorkSchedule]:
        schedules = WorkSchedule.objects.filter(store_id=store_id).all()
        return list(schedules)

    def get_detail_schedules_by_id(self, id: int, store_id: int) -> WorkSchedule:
        try:
            schedule = WorkSchedule.objects.get(id=id, store_id=store_id)
            return schedule
        except WorkSchedule.DoesNotExist:
            return None

    def create_schedule_of_staff(
        self, schedule_id: int, data, user_id
    ) -> None:
        s_work_schedule = S_WorkSchedule.objects.create(
        work_day=data['work_day'],
        shift=data['shift'],
        description=data['description'],
        user_id=user_id,
        work_schedule_id = schedule_id,
    )
        return s_work_schedule


    def due_schedule(self, schedule_id: int )-> bool:
        given_date = datetime.now().date()
        work_schedule = get_object_or_404(WorkSchedule, id=schedule_id)
        start_day = work_schedule.start_day.strftime("%d-%B-%Y")
        end_day = work_schedule.closing_date.strftime("%d-%B-%Y")
        if given_date >= start_day and given_date <= end_day:
            return True
        return False
    
    def get_all_schedule_for_staff(self,schedule_id: int ) -> List[WorkSchedule]:
        schedules = S_WorkSchedule.objects.filter(work_schedule_id = schedule_id).all()
        return list(schedules)
    
    def update_schedule_of_staff(self, schedule_id: int, data) -> None:
        s_work_schedule = S_WorkSchedule.objects.get(id=schedule_id)
        s_work_schedule.work_day = data['work_day']
        s_work_schedule.shift = data['shift']
        s_work_schedule.description = data['description']
        s_work_schedule.save()
        return s_work_schedule
    
    def delete_schedule_of_staff(self, id: int) -> None:
        s_work_schedule = S_WorkSchedule.objects.get(id=id)
        s_work_schedule.delete()
        return s_work_schedule
    
    def get_day_of_week(self,date_string):
        day_index = date_string.weekday()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[day_index]
    
    def create_schedule_of_owner(
        self, schedule_id: int, s_schedule_id: int 
    ) -> None:
        s_workSchedule = S_WorkSchedule.objects.filter(id = s_schedule_id).first()
        staff_id = s_workSchedule.user_id
        staff_name = User.objects.get(id=staff_id).username
        work_day = s_workSchedule.work_day
        shift = s_workSchedule.shift
        description = s_workSchedule.description
        week_day = self.get_day_of_week(work_day)
        
        o_workSchedule = O_WorkSchedule.objects.create(
            staff_name = staff_name,
            work_day = work_day,
            shift = shift,
            description = description,
            week_day = week_day,
            work_schedule_id = schedule_id,
            s_work_schedule_id = s_schedule_id,
            )
        return o_workSchedule
    
    def delete_schedule_of_owner(self, id: int) -> None:
        o_workSchedule = O_WorkSchedule.objects.get(id=id)
        o_workSchedule.delete()
        return o_workSchedule

    
        
        
    
        