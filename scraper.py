from bs4 import BeautifulSoup
import requests

url = "https://www.sports.ru/"
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")
def get_games():
    events = soup.find_all("div", {"class":"accordion__handle"})
    all_data = []
    # time = []
    # first_teams = []
    # scores = []
    # second_teams = []
    for event in events:
        event_name =event.find("span", {"class":"accordion__title"}).find("a").text
        if "футбол" in event_name:
            matches = event.findNext("div").find_all("li")
            for match in matches:

                status = match.find("div").find("span").text
                score_and_teams = match.find("div", {'class':'teaser-event__board'})
                teams = score_and_teams.find_all("div", {"class": "teaser-event__board-player"})
                team1 = teams[0].find("a").text
                team2 = teams[1].find("a").text
                score = match.find("a", {"class":"teaser-event__board-score"}, href=True)
                if score['href'][0] == '/':
                    minute_url = "https://www.sports.ru"+score['href']
                else:
                    minute_url = score['href']
                # minute_url = url+score['href'][1:]
                all_data.append([status, team1, score.text, team2, minute_url, event_name])
    return all_data

def get_scorers(url):

    r_ = requests.get(url)
    c_ = r_.content
    soup_ = BeautifulSoup(c_, "html.parser")
    #time = BeautifulSoup('<svg></svg>','xml')
    current_minute = ""
    #minute_tag = soup_.find("svg", {"class":"timer"})
    match_summary = soup_.find("div", {"class": "match-summary"})
    #minute_tag = time.find("text", {"class":"timer__text"})
    # minute_tag = match_summary.find("svg", {"class":"timer"})

    all_team_info = [[],[]]
    if match_summary:
        teams = match_summary.find_all("div", {"class":"match-summary__team"})
        for i in range(len(teams)):
            team = teams[i]
            goals = team.find("ul", {"class":"match-summary__goals-list"})
            if goals:
                goal_list = goals.find_all("li")
                for j in range(len(goal_list)):
                    goal = goal_list[j]
                    minute=""
                    scorer = ""
                    # if goal.find("span", {"class":"match-summary__goal-time"}):
                    #     if goal.find("span", {"class":"match-summary__goal-time"}).find("span"):
                    #         minute+="*"
                    if goal.find("span", {"class":"match-summary__goal-time"}):
                        minute += goal.find("span", {"class":"match-summary__goal-time"}).text
                    if goal.find("span", {"class":"match-summary__goal-scorer"}):
                        scorer = goal.find("span", {"class":"match-summary__goal-scorer"}).text
                    if goal.find("span", {"class": "match-summary__goal-assist"}):
                        assistant = goal.find("span", {"class": "match-summary__goal-assist"}).text
                    else:
                        assistant = ""
                    if minute!="" or scorer!="" or assistant!="":
                        all_team_info[i].append([minute, scorer,assistant])
                    
                    
    return all_team_info, current_minute
            
