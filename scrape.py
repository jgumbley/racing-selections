from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

response = urlopen("http://www.racingpost.com/horses2/cards/card.sd?race_id=526624&r_date=2011-04-10")
html = response.read()

print html
