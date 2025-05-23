from fastapi import APIRouter
from app.services.fpl import fetch_team_from_fpl
from app.schemas.plan import PlanCreate
from app.services.planner import create_plan

router = APIRouter()
USER_ID = 2322892  # Replace with your actual FPL ID

@router.get("/team/current")
async def get_current_team():
    data = await fetch_team_from_fpl()
    picks = data.get("picks", [])
    return [{"player_id": p["element"], "is_captain": p["is_captain"]} for p in picks]


@router.post("/plan")
async def create_new_plan(plan: PlanCreate):
    return await create_plan(USER_ID, plan.title)