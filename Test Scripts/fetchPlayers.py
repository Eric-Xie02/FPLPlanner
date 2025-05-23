import requests

def fetch_all_players():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    res = requests.get(url)
    data = res.json()

    players = data['elements']
    teams = {team['id']: team['name'] for team in data['teams']}
    positions = {pos['id']: pos['singular_name'] for pos in data['element_types']}

    for player in players[:10]:  # Show just first 10 players for example
        name = f"{player['first_name']} {player['second_name']}"
        team = teams[player['team']]
        pos = positions[player['element_type']]
        price = player['now_cost'] / 10
        print(f"{name} | {pos} | {team} | £{price}m")

if __name__ == "__main__":
    fetch_all_players()
