import requests


def show_team_info(user_team: str):
    # api al all nba teams
    all_teams_api = "https://www.balldontlie.io/api/v1/teams"

    # response from the selected url
    response = requests.get(all_teams_api)

    if response.status_code == 200:
        # getting data from API
        data = response.json()

        # getting specific team info with the following key
        for team in data["data"]:
            if team["full_name"] == user_team:
                return team
    return False
