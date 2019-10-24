# Carolyn Sullivan, Oct. 23-24, 2019
# Base code originated from https://github.com/amanthedorkknight/fifa18-all-player-statistics/blob/master/2019/crawler.py
# which tried to scrape data from: https://sofifa.com/players?offset=
# A script which scrapes compact statistics relevant to the market value of football players from
# https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&plus=1

import pandas as pd                 # open-source data analysis library
import re                           # regular expression library
import requests                     # allows sending of HTTP/1.1 requests
from bs4 import BeautifulSoup       # For pulling data out of HTML and XML files

# Get basic players information for all players
# @base_url     The url at which the data is found.
# @columns      The names you would like to appear for the variables you're gathering from the webpage.
# @data         The pandas dataframe; the dataframe is a tabular labelled data structure
base_url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/ausrichtung/alle/spielerposition_id/alle/altersklasse/alle/jahrgang/0/land_id/0/yt0/Show/0/"
columns = ['PlayerName', 'Position', 'Age', 'Nationality', 'Club', 'MarketValue']
data = pd.DataFrame(columns = columns)

# The original script iterated from 0 to 300, because the sofifa page it scraped the data from tabulated the first 300
# players and had 60 players per page--implying the first player on the next page was at offset*61.
# Oddly though, the URL isn't changing for the Fifa webpage even when I click to another page, which would seem
# to indicate it's all on a single page.

# For source_code, have to change default value of headers to access with Python script.

for offset in range(0,20): # Use range 20 as there are 20 pages of data.
    if offset==0:
        url = base_url
    else:
        url = base_url + "/page/" + str(offset + 1) # The url is edited to access pages after the first page.
    print(url)
    source_code = requests.get(url, headers={'User-Agent': 'Custom'})    # Returns an HTTP request response (ie. 200, 404).
    plain_text = source_code.text           # Retrieve the text in the source code?
    soup = BeautifulSoup(plain_text, 'html.parser')
    table_body = soup.findAll('tbody')  # Takes the contents of the table from each page.
    playerTable = table_body[1]
    print(playerTable)
    playerRows = playerTable.findAll('tr')   # Grabs all the "tr".  Technically just need "tr class="odd", but for some reason it won't let me access just that.  TODO: Find out why.
    count = 0   #dummy variable to make sure only taking every THIRD object in the playerRows list (otherwise, format of row is incorrect for this script)

    print( str(len(playerRows)) )

    for row in playerRows:                # .findAll returns a list of table rows, iterate over these (cleaner to find once?)
        if count%3 == 0:                    #get correctly formatted row
            td = row.findAll('td')                          # row.findAll returns lists of all text between tags
            print(td)                         # Gives first page of data anyways...
            PlayerName = td[3].text
            #print(td[1])
            #print(td[1].find("img"))
            print(PlayerName)
            Position = td[4].text
            print(Position)
            Age = td[5].text
            print(Age)
            Nationality=td[6].find("img").get("alt")
            print(Nationality)
            Club = td[7].find("img").get("alt")
            print(Club)
            MarketValue = td[8].text
            print(MarketValue)

            player_data = pd.DataFrame([[PlayerName, Position, Age, Nationality, Club, MarketValue]])   #Shove values in dataframe.
            player_data.columns = columns   #associate player data columns with the columns used in our larger dataframe.
            data = data.append(player_data, ignore_index=True) #add the playerdata to the larger data.
        count+=1 # increment dummy variable.

data.to_csv('data.csv', encoding='utf-8-sig')   #Place in Csv file
