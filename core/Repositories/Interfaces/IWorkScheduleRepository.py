from typing import List
from abc import ABC, abstractmethod
from  WorkSchedule.models import WorkSchedule


class WorkScheduleRepository(ABC):
    @abstractmethod
    def create_schedules_by_store_id(self, store_id: int) -> None:
        pass
    
    def get_all_schedules_by_store_id(self, store_id: int)-> None:
        pass
    
    def get_detail_schedules_by_store_id(self, store_id: int)-> None:
        pass