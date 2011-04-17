from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request
from urllib import quote as urlencode
from simplejson import load as loadjson
from datetime import datetime
import inspect

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
        m = inspect.getmembers(self, predicate=inspect.ismethod)
        for item in m:
            if str(item[0])[:6] in "scrape":
                item[1]()

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

    def scrapeMeetingDetails(self):
        meeting = self.soup.findAll("h1", {"class": "cardHeadline"})[0]
        self.location = meeting.contents[2].strip()

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
            meetings.append( ( nag , scrape.location) )
    return meetings


googlenewsurl = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0" + \
        "&q=SEARCH&key=ABQIAAAAyABxmfS34tEMlt2UD9HT2hSN4OZNJRcNb-mTkbWyVBE6-ADJ1BSpSdvs_0bBvtx5eI3evqY9t0U4rA&userip=87.113.4.205"

def pressMentions(term):
    enc_term = urlencode('source:"racing post" "' + term + '"')
    request = urlopen(googlenewsurl.replace("SEARCH", enc_term))
    results = loadjson(request)
    try:
        return results["responseData"]['cursor']['estimatedResultCount']
    except: 
        return 0

def doWork():
    session = Session()
    for runn in getMeetings():
        run = Run(runn[0], runn[1], "12:00")
        print run
        session.merge(run)
    session.commit()

doWork()
