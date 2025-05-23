from app.database import db
from datetime import datetime
import httpx
from app.schemas.plan import GWSquad, PlanCreate
from bson import ObjectId

FPL_ID = 2322892

async def fetch_fpl_team():
    async with httpx.AsyncClient() as client:
        # Step 1: Get current gameweek number
        bootstrap_res = await client.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        bootstrap_data = bootstrap_res.json()
        current_event = next((e for e in bootstrap_data["events"] if e["is_current"]), None)
        if current_event is None:
            raise ValueError("Unable to determine current gameweek")

        current_gw = current_event["id"]
        next_gw = current_gw + 1

        # Step 2: Get user picks and team info
        picks_res = await client.get(f"https://fantasy.premierleague.com/api/entry/{FPL_ID}/event/{current_gw}/picks/")
        team_res = await client.get(f"https://fantasy.premierleague.com/api/entry/{FPL_ID}/")

        picks = picks_res.json()
        team_info = team_res.json()

    return picks, team_info, next_gw

async def create_plan(user_id: str, title: str):
    picks, team_info, next_gameweek = await fetch_fpl_team()

    # Estimate next gameweek based on last history
    next_gameweek = picks["entry_history"]["event"] + 1

    team_ids = [p["element"] for p in picks["picks"]]
    captain_id = next((p["element"] for p in picks["picks"] if p["is_captain"]), team_ids[0])

    starter_squad = GWSquad(
        gameweek=next_gameweek,
        team=team_ids,
        captain_id=captain_id,
        free_transfers=1,
        budget=1000,
        active_chip=None,
        assistant_manager=None,
        ass_man_remaining_weeks=None,
        notes=None,
        assistant_manager_available=True,
        wildcard_available=True,
        benchboost_available=True,
        triple_captain_available=True,
        freehit_available=True,
    )

    plan = {
        "user_id": user_id,
        "title": title,
        "created_at": datetime.utcnow(),
        "gw_squads": [starter_squad.dict()]
    }

    result = await db.plans.insert_one(plan)
    plan["_id"] = str(result.inserted_id)
    return plan

async def fetch_user_plans(user_id: str):
    cursor = db.plans.find({"user_id": user_id})
    plans = await cursor.to_list(length=None)

    for plan in plans:
        plan["_id"] = str(plan["_id"])

    return plans

async def fetch_plan(id: str):
    plan = await db.plans.find_one({"_id": ObjectId(id)})

    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan["_id"] = str(plan["_id"])
    return plan