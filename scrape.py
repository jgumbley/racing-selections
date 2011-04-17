from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request
from urllib import quote as urlencode
from simplejson import load as loadjson

from persist import Session, Nag, Run

def soupUp(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

def getNags(url):
    soup = soupUp(url)
    nags = []
    for horsesoup in soup.findAll("table", {"class":'cardSt'}):
        for possiblehorse in horsesoup.findAll("b"):
            if len(possiblehorse.text) > 5:
                nags.append(possiblehorse.text.strip())
    return nags

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


def getMeetingDetails(url):
    soup = soupUp(url)
    meeting = soup.findAll("h1", {"class": "cardHeadline"})[0]
    return meeting.contents[2].strip()


todayurl = "http://www.racingpost.com/horses2/cards/home.sd?r_date=2011-04-17"

def getTodaysRunners():
    nags = []
    for cardurl in getTodaysRaces(todayurl):
        nags.extend(getNags(cardurl))
    return nags

def getMeetings():
    meetings = []
    for cardurl in getTodaysRaces(todayurl):
        location = getMeetingDetails(cardurl)
        for nag in getNags(cardurl):
            meetings.append( ( nag , location) )
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
