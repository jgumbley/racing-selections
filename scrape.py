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
        self.cardurls = []
        for cardsoup in self.soup.findAll("td", {"class": 'crd bull'}):
            try:
                cardurl = cardsoup.contents[1]["href"]
                self.cardurls.append(cardurl)
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
                    nags.append(possiblehorse.text.strip())
        self.runners = nags

def getMeetings():
    meetings = []
    for cardurl in RPTodayRaces(datetime.now()).cardurls:
        scrape = RPRaceCard( cardurl )
        for nag in scrape.runners:
            meetings.append( ( nag , scrape.location, scrape.time) )
    return meetings

def doWork():
    session = Session()
    for runn in getMeetings():
        run = Run(runn[1], runn[0], runn[2])
        print run
        session.merge(run)
    session.commit()

doWork()
