
from ics import Calendar, Event
from bs4 import Tag, NavigableString, BeautifulSoup
import re
import pprint
import arrow

re_week = re.compile(r'^([A-Z]*).*Woche\s(\d+).*')


re_training = re.compile(r'^(\d)[a-z]*[:\.]\s.*')


c = Calendar()



def is_week(row):
    title_rex = re_week.match(row.text)
    if title_rex: 
        return True
    return False

def out_training(training):
    ergs = re_training.match(training['title'])
    training_nr = int(ergs[1])
    print("%2i %2s - %-60s - %10s - %s - %s - %s"%(
        training['week'],
        training_nr,
        training['title'],
        training['dauer'],
        training['pulswert'],
        training['tempo'],
        training['strecke']  
    ))

    e = Event()
    e.name = training['title']
    begin = arrow.get('2019-09-22T18:00:00')
    e.begin = begin.shift(days=(training_nr-1)*2, weeks=training['week']-1)
    e.description = "Dauer: %s\nPuls: %s\nTempo: %s\nStrecke: %s\n\n%s"%(
        training['dauer'],
        training['pulswert'],
        training['tempo'],
        training['strecke'],
        'loDL: lockerer Dauerlauf - LDL: langer Dauerlauf, Longjog - laDL: langsamer Dauerlauf - züDL: zügiger Dauerlauf - TDL: Tempodauerlauf - IV: Intervalltraining, Intervalle - TP: Trabpausen, Gehpausen - EL: Einlaufen, aufwärmen - AL: cool down, auslaufen.'
        )
    e.make_all_day()
    c.events.add(e)
    c.events


def parse_training(week, row):
    tds = row.find_all('td')
    title = tds[0]
    if not re_training.match(title.text):
        return

    titles = ' '.join([i for i in title.contents if isinstance(i,NavigableString)])
    dauer = ' '.join([i for i in  tds[1].contents if isinstance(i,NavigableString)])
    pulse = ' / '.join([i for i in  tds[2].contents if isinstance(i,NavigableString)])
    tempos = ' / '.join([i for i in  tds[3].contents if isinstance(i,NavigableString)])
    strecken = ' '.join([i for i in  tds[4].contents if isinstance(i,NavigableString)])

    
    training = {
        'title' : titles,
        'dauer' : dauer,
        'pulswert' : pulse,
        'tempo' : tempos,
        'strecke' : strecken
    }

    training.update(week)
    out_training(training)


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



# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
with open('laufplan.ics', 'w') as my_file:
    my_file.writelines(c)
# and it's done !
