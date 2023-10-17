import requests
import pprint


def show_team_info(user_team: str):
    # for structured data printing
    pp = pprint.PrettyPrinter(indent=4)

    # api al all nba teams
    all_teams_api = "https://www.balldontlie.io/api/v1/teams"

    # response from the selected url
    response = requests.get(all_teams_api)

    if response.status_code == 200:
        # getting data from API
        data = response.json()
        pp.pprint(data["data"])

        for team in data["data"]:
            if team["full_name"] == user_team:
                return team
    return False
