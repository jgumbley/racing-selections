from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen


def soupUp(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

url="http://www.racingpost.com/horses2/cards/card.sd?race_id=526624&r_date=2011-04-10"

def getNags(url):
    soup = soupUp(url)
    for horsesoup in soup.findAll("table", {"class":'cardSt'}):
        for possiblehorse in horsesoup.findAll("b"):
            if len(possiblehorse.text) > 5:
                print possiblehorse.text.strip() 

todayurl = "http://www.racingpost.com/horses2/cards/home.sd?r_date=2011-04-10"

def getTodaysRaces(url):
    soup = soupUp(url)
    cardurls = []
    for cardsoup in soup.findAll("td", {"class": 'crd bull'}):
        try:
            cardurl = cardsoup.contents[1]["href"]
            cardurls.append(cardurl)
        except:
            continue
    return cardurls

for cardurl in getTodaysRaces(todayurl):
    getNags(cardurl)


