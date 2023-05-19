# Importation

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests 
import pandas as pd
import numpy as np

name = []
platform = []
date = []
metascore = []
userscore = []
url = []

page = 0

# There are 203 pages
while page != 203:

    link = f"https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page={page}"
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    response = session.get(link)

    soup = bs(response.content,'html.parser')

    games = soup.find_all("td", class_="clamp-summary-wrap")

    for element in games :

        # Names & URL
        try:
            if element.find("a", class_='title'):
                name.append(element.find("a", class_='title').text.strip())
                url.append(element.find("a", class_='title').get("href"))
            elif element.find("a", class_='title') == None :
                name.append(np.nan)
                url.append(np.nan)
        except:
            name.append(np.nan)
            url.append(np.nan)

        # Platform
        try:
            if element.find("div", class_="platform").find("span", class_="data"):
                platform.append(element.find("div", class_="platform").find("span", class_="data").text.strip())
            elif element.find("div", class_="platform").find("span", class_="data") == None :
                platform.append(np.nan)
        except:
            platform.append(np.nan)
        
        # Date
        try:
            if element.find("div", class_="clamp-details").find_all('span')[-1]:
                date.append(element.find("div", class_="clamp-details").find_all('span')[-1].text.strip())
            elif element.find("div", class_="clamp-details").find_all('span')[-1] == None:
                date.append(np.nan)
        except:
            date.append(np.nan) 

        # Metascore
        try:
            if element.find('div',class_="metascore_w large game positive"):
                metascore.append(element.find('div',class_="metascore_w large game positive").text.strip())
            elif element.find('div',class_="metascore_w large game mixed"):
                metascore.append(element.find('div',class_="metascore_w large game mixed").text.strip())

            elif element.find('div',class_="metascore_w large game negative"):
                metascore.append(element.find('div',class_="metascore_w large game negative").text.strip())
            else :
                metascore.append("0")
        except:
            metascore.append(np.nan)
        
        # Userscore
        try:
            if element.find('div',class_="metascore_w user large game positive"):
                userscore.append(element.find('div',class_="metascore_w user large game positive").text.strip())
            elif element.find('div',class_="metascore_w user large game mixed"):
                userscore.append(element.find('div',class_="metascore_w user large game mixed").text.strip())
            elif element.find('div',class_="metascore_w user large game negative"):
                userscore.append(element.find('div',class_="metascore_w user large game negative").text.strip())
            else :
                userscore.append(np.nan)
        except:
            userscore.append(np.nan)

    page+=1

df = pd.DataFrame({"Name":name,
                   "Platform":platform,
                   "Date":date,
                   "Metascore":metascore,
                   "Userscore":userscore,
                   "URL":url})

#df.to_csv('metacritic.csv', index = False)