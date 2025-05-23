from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GWSquad(BaseModel):
    gameweek: int
    team: List[int]
    captain_id: int
    free_transfers: int
    budget: int
    active_chip: Optional[str] = None
    assistant_manager: Optional[str] = None
    ass_man_remaining_weeks: Optional[int] = None
    notes: Optional[str] = None
    assistant_manager_available: bool
    wildcard_available: bool
    benchboost_available: bool
    triple_captain_available: bool
    freehit_available: bool


class PlanCreate(BaseModel):
    title: str
    gw_squads: Optional[List[GWSquad]] = None

class PlanResponse(PlanCreate):
    user_id: str
    created_at: datetime