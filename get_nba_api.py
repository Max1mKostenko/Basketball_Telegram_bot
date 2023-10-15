import requests
import pprint


# for structured data printing
pp = pprint.PrettyPrinter(indent=4)

# api al all nba teams
all_teams_api = "https://www.balldontlie.io/api/v1/teams"

# api of specific team
team_id = 14
specific_team_api = f"https://www.balldontlie.io/api/v1/teams/{team_id}"

# response from the selected url
response = requests.get(all_teams_api)

if response.status_code == 200:
    # getting data from API
    data = response.json()
    pp.pprint(data)
else:
    print(f"Failed to get data. Status code: {response.status_code}")
