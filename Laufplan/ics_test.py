
from ics import Calendar, Event
from bs4 import Tag, NavigableString, BeautifulSoup
import re
import pprint

re_week = re.compile(r'^([A-Z]*).*Woche\s(\d+).*')
re_training = re.compile(r'^\d[a-z]*[:\.]\s.*')


def is_week(row):
    title_rex = re_week.match(row.text)
    if title_rex: 
        return True
    return False

def parse_training(week, row):
    tds = row.find_all('td')
    title = tds[0]
    if not re_training.match(title.text):
        return
    dauer = tds[1]
    training = {
        'title' : title.text,
        'dauer' : dauer.text
    }
    training.update(week)
    print("%2i - %-100s - %s"%(
        training['week'],
        training['title'],
        training['dauer']
    ))


def parse_week(wdata):
    title = wdata.next_element
    if not is_week(title):
        return

    title_rex = re_week.match(title.text)
    special = title_rex[1].strip(' ')
    week_nr = int(title_rex[2])
 
    week ={
        'special' : special,
        'week' : week_nr
    }
    sibling = wdata.next_sibling

    while isinstance(sibling.next_element, Tag) and (not is_week(sibling.next_element)): 
        parse_training(week, sibling)
        sibling = sibling.next_sibling
        while not isinstance(sibling, Tag):
            sibling = sibling.next_sibling
soup = None
with open('Laufplan.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

cla = soup.find_all("tr",{'class':'yell'})
for i in cla:
    parse_week(i)

c = Calendar()
e = Event()
e.name = "My cool event"
e.begin = '2019-09-23 00:00:00'
c.events.add(e)
c.events

e = Event()
e.name = "My cool event 2"
e.begin = '2019-09-24 00:00:00'
c.events.add(e)
c.events

# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
with open('laufplan.ics', 'w') as my_file:
    my_file.writelines(c)
# and it's done !
