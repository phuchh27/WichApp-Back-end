from WorkSchedule.models import WorkSchedule
from core.Repositories.Interfaces.IWorkScheduleRepository import WorkScheduleRepository
from datetime import datetime, timedelta
from calendar import month_name
from typing import List

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