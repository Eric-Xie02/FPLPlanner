import requests

def get_current_gameweek():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    data = requests.get(url).json()
    for event in data["events"]:
        if event["is_current"]:
            return event["id"]
    raise ValueError("Could not determine current gameweek")

def get_player_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    data = requests.get(url).json()

    player_map = {}
    team_map = {team["id"]: team["name"] for team in data["teams"]}
    position_map = {etype["id"]: etype["singular_name"] for etype in data["element_types"]}

    for p in data["elements"]:
        player_map[p["id"]] = {
            "name": f"{p['first_name']} {p['second_name']}",
            "team": team_map[p["team"]],
            "position": position_map[p["element_type"]],
            "price": p["now_cost"] / 10,
        }
    return player_map

def get_team(entry_id, gameweek, player_map):
    picks_url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gameweek}/picks/"
    res = requests.get(picks_url)
    if res.status_code != 200:
        raise ValueError(f"Failed to fetch picks for GW{gameweek}")
    picks = res.json()["picks"]

    print(f"\n📋 Your Full FPL Team for Gameweek {gameweek}:\n")

    for i, pick in enumerate(picks):
        player_id = pick["element"]
        mult = pick["multiplier"]
        is_captain = pick["is_captain"]
        is_vice = pick["is_vice_captain"]

        pdata = player_map.get(player_id, {})
        name = pdata.get("name", "Unknown")
        pos = pdata.get("position", "?")
        price = pdata.get("price", "?")

        tag = ""
        if is_captain:
            tag = "(C)"
        elif is_vice:
            tag = "(VC)"
        elif mult == 0:
            tag = "(Bench)"
        else:
            tag = "(XI)"

        print(f"{name:<25} | {pos:<4} | £{price:.1f}m | {tag}")

if __name__ == "__main__":
    entry_id = 2322892  # Your FPL team ID
    gw = get_current_gameweek()
    player_map = get_player_data()
    get_team(entry_id, gw, player_map)
