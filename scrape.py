from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

url="http://www.racingpost.com/horses2/cards/card.sd?race_id=526624&r_date=2011-04-10"

def getNags(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    for horsesoup in soup.findAll("table", {"class":'cardSt'}):
        for possiblehorse in horsesoup.findAll("b"):
            if len(possiblehorse.text) > 5:
                print possiblehorse.text.strip() 


getNags(url)
