from persist import Session, Nag, Run
from scrape import RPTodayRaces, RPRaceCard
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from logbook import info, warn, error

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
            warn("url=" + meetingURL + " " + str(e))
    return runs

def doWork():
    session = Session()
    for run in scrapeRuns():
        try:
            session.merge(run)
            session.commit()
        except IntegrityError:
            error("Duplicate Run: " + str(run))
            session.rollback()

if __name__=='__main__':
    info("script='do_daily' event='start'")
    doWork()
