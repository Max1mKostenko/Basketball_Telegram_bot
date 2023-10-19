import requests
from bs4 import BeautifulSoup


def get_nba_news(fav_team_name):
    # empty list, to collecting all urls
    news_list = []

    if fav_team_name == "mavericks":
        news_list.append("https://www.mavs.com/")
        return news_list

    if fav_team_name == "76ers":
        news_list.append("https://www.nba.com/sixers/")
        return news_list

    elif fav_team_name == "trail blazers":
        fav_team_name = "blazers"

    URL = f"https://www.nba.com/{fav_team_name}/news/"

    # get content of the page
    response = requests.get(URL)

    if response.status_code != 200:
        print("Failed get data from site")
        return False

    # pars the content from site
    soup = BeautifulSoup(response.content, "html.parser")

    # saving list with tags <a> and specific class
    news_items = soup.find_all("a", class_="TileArticle_tileLink__9vE5P")

    for item in news_items:
        link = f"https://www.nba.com{item['href']}"
        news_list.append(link)

    return news_list
