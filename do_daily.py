from persist import Session, Nag, Run
from scrape import RPTodayRaces, RPRaceCard
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def scrapeRuns():
    runs = []
    today = datetime.now()
    for meetingURL in RPTodayRaces(today).cardurls:
        try:
            race_card = RPRaceCard(meetingURL)
            for nag in race_card.runners:
                runs.append(
                        Run( nag["name"] , race_card.location, race_card.time)
                        )
        except Exception, e:
            print e
    return runs

def doWork():
    session = Session()
    for run in scrapeRuns():
        try:
            session.merge(run)
            session.commit()
        except IntegrityError:
            print "Duplicate Run: " + str(run)
            session.rollback()

if __name__=='__main__':
    doWork()
