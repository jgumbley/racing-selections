from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request
from datetime import datetime
from inspect import getmembers, ismethod

from persist import Session, Nag, Run

def soupUp(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

class Scraper(object):
    def doInit(self, url):
        self.url = url
        self.soup = soupUp(url)
        self.doScrape()

    def doScrape(self):
        """This introspects all methods of the class and calls ones which 
        start with scrape. I suppose this might be problematic if you used 
        multiple inheritance but at the moment I don't care.
        """
        methods = getmembers(self, predicate=ismethod)
        for method in methods:
            if str(method[0])[:6] in "scrape":
                method[1]()

class RPTodayRaces(Scraper):
    todayurl = "http://www.racingpost.com/horses2/cards/home.sd?r_date="

    def __init__(self, date):
        self.doInit( self.todayurl + date.isoformat()[:10] )

    def scrapeTodaysRaces(self):
        self.cardurls = set() # use set to dedupe
        for cardsoup in self.soup.findAll("td", {"class": 'crd bull'}):
            try:
                cardurl = cardsoup.contents[1]["href"]
                self.cardurls.add(cardurl)
            except:
                continue
        
class RPRaceCard(Scraper):
    def __init__(self, url):
        self.doInit( url )

    def scrapeLocationAndTime(self):
        meeting = self.soup.findAll("h1", {"class": "cardHeadline"})[0]
        self.location = meeting.contents[2].strip()
        timesoup = meeting.findAll("span")
        self.time = timesoup[0] 
        if len(timesoup[0].contents) == 3:
            if timesoup[0].contents[0].strip() not in "":
                self.time = timesoup[0].contents[0].strip()
            else: 
                self.time = timesoup[0].contents[2].strip()
        else:
            self.time = timesoup[0].contents[2].strip()
        if self.time in '':
            raise Exception

    def scrapeNags(self):
        nags = []
        for horsesoup in self.soup.findAll("table", {"class":'cardSt'}):
            for possiblehorse in horsesoup.findAll("b"):
                if len(possiblehorse.text) > 5:
                    nag = {}
                    nag["name"] = possiblehorse.text.strip()
                    nag["odds"] = 0
                    nags.append(nag)
        self.runners = nags

#card = RPRaceCard("http://www.racingpost.com/horses2/cards/card.sd?race_id=527785&r_date=2011-04-23")

#print card.runners

