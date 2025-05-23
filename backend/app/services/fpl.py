import httpx

FPL_ID = 2322892  # Replace with your actual FPL ID

async def fetch_team_from_fpl():
    url = f"https://fantasy.premierleague.com/api/entry/{FPL_ID}/event/36/picks/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

