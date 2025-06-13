from pydantic import BaseModel, Field, validator
from typing import Union, List, Optional
from datetime import time, date
import json


class ScheduleCreateRequest(BaseModel):
    line_id: int
    trasy_id: Optional[int] = None
    brygada_id: Optional[int] = None
    autobus_id: Optional[int] = None
    kierowca_id: Optional[int] = None
    data_od: date
    data_do: date
