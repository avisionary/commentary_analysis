from requests import get
from bs4 import BeautifulSoup
import datetime
import regex as re
import pandas as pd
from unidecode import unidecode

class Scrapper():
    """
        Class for Scraping a Goal.com website for further analysis
    """
    def __init__(self,url,match):
        self.match = match
        self.url = url
        self.log = []

    def __str__(self) -> str:
        return f"Scraping for {self.match} from {self.url}"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({str(self)})>"
    
    def scrap(self):
        #get data from site
        print(f"Scraping for this match : {self.match}")
        response = get(self.url,headers= {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} )

        #print status code

        print(response.status_code)

        if response.status_code == 200:
            pageSoup = BeautifulSoup(response.content, 'html.parser')
            time = []
            comment = []
            event = []
            event_player = []
            event_team = []
            comment_desc = []

            half_time_flag = False
            timer_flag = False
            comment_desc_dict = {True: "half time summary",
                            False : "full time summary"}

            counter = 0

            for x in pageSoup.findAll('div',class_ = "comment"):
                counter += 1

                if x.find_all("div", {"class": "comment-event"}):
                    for q in x.findAll('div',class_ = "wrapper"):
                        for r in q.findAll('div',class_ = "event-icon"):
                            e = r.find("div")["class"][1]
                            e = e.replace("type-","")
                            e = unidecode(e)
                            

                        for r in q.findAll('div',class_ = "event-text has-additional"):
                            if r.find("div",{"class" : "event-text-main" }):
                                p1 = unidecode(r.find("div",{"class" : "event-text-main" }).text)
                            else:
                                p1 = ""
                            if r.find("div",{"class" : "event-text-additional" }):
                                p2 = unidecode(r.find("div",{"class" : "event-text-additional" }).text)
                                #e = x.find("div", {"class": "comment-event"}).find("event-text-additional").text
                            else:
                                p2 = ""
                            

                        for r in q.findAll('div',class_ = "event-crest"):
                            for d in r.findAll('a'):
                                #print(d)
                                te = unidecode(d.find("img")['alt'])
                                

                    event_player.append([p1,p2])
                    event.append(e)
                    event_team.append(te)


                else:
                    event.append("")
                    event_player.append("")
                    event_team.append("")
                for y in x.findAll('div',class_ = "comment-desc"):
                    if y.find_all("span", {"class": "time"}):
                        timer_flag = True


                        t = y.find('span',class_ = "time").text
                        t = t.replace("'","")
                        #print(t)
                        time.append(t)
                        comment_desc.append("timer")
                    else:
                        time.append("")
                        if time[-1] == "" and timer_flag:
                                half_time_flag = True
                        comment_desc.append(comment_desc_dict[half_time_flag])
                        #print("Summary")
                    
                    if y.find_all("span", {"class": "text"}):
                        c = y.find('span',class_ = "text").text
                        c = unidecode(c)
                        comment.append(c)
            

            print(f"Total scraped comments for this match: {counter} ")
            match_commentary_df = pd.DataFrame(list(zip(time, comment,event,event_player,event_team,comment_desc)),
                    columns =['time', 'comment','event','event_player','event_team','comment_desc'])
            
            team_count = 0
            for teams in pageSoup.findAll('div',class_ = "widget-match-header__name"):
                if team_count == 0:
                    match_commentary_df['home_team'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--full" }).text)
                    match_commentary_df['home_team_abbr'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--short" }).text)
                    team_count += 1
                elif team_count == 1:
                    match_commentary_df['away_team'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--full" }).text)
                    match_commentary_df['away_team_abbr'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--short" }).text)

            for score in pageSoup.findAll('div',class_ = "widget-match-header__score"):
                match_commentary_df['full_time_score'] = unidecode(score.find("span").text)
            

            return (match_commentary_df,1)
        else:
            self.log.append(self.match)
            return (0,0)

