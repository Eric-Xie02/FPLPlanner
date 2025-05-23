from fastapi import APIRouter
from app.services.fpl import fetch_team_from_fpl
from app.schemas.plan import PlanCreate
from app.services.planner import create_plan, fetch_user_plans, fetch_plan

router = APIRouter()
USER_ID = 2322892  # Replace with your actual FPL ID

@router.get("/team/current")
async def get_current_team():
    data = await fetch_team_from_fpl()
    picks = data.get("picks", [])
    return [{"player_id": p["element"], "is_captain": p["is_captain"]} for p in picks]


@router.post("/plan/{user_id}")
async def create_new_plan(plan: PlanCreate, user_id: str):
    return await create_plan(user_id, plan.title)


@router.get("/plans/{user_id}")
async def get_user_plans(user_id: str):
    return await fetch_user_plans(user_id)

@router.get("/plan/{plan_id}")
async def get_plan(plan_id: str):
    return await fetch_plan(plan_id)
