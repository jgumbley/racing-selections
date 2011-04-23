from persist import Session, Nag, Run
from scrape import RPTodayRaces, RPRaceCard
from datetime import datetime

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

if __name__=='__main__':
    doWork()
