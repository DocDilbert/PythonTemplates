import json
import pprint
with open("ss.json", encoding="utf-8") as fp:
    raw_data = json.load(fp)

data = {}
for entry in reversed(raw_data):
    uuid = entry['uuid']
    entry.pop('uuid',None) # remove uuid
    entry_without_id= dict(entry)
    entry_without_id.pop('session_id', None)
    if uuid in data:
        last = data[uuid][-1]
        last_without_id = dict(last)
        last_without_id.pop('session_id', None)

        if last_without_id != entry_without_id:
            data[uuid].append(entry)
    else:
        data[uuid]= []
        data[uuid].append(entry)

for key, _ in data.items():
    data[key]=list(reversed(data[key]))

max_session_id = max((
    i['session_id'] for _, l in data.items() for i in l
))



removed = {
    k:i[-1] for k, i in data.items() if i[-1]['session_id']!=max_session_id
}

removed_dict = {}

for key, entry in removed.items():
    session_id = entry['session_id']
    entry_copy = dict(entry)
    entry_copy.pop('session_id', None)
    if session_id in removed_dict:
        removed_dict[session_id].update({key:entry_copy})
    else:
        removed_dict[session_id] = {}
        removed_dict[session_id].update({key:entry_copy})
 


up_to_date = {
    k:i[-1] for k, i in data.items() if i[-1]['session_id']==max_session_id
}

parsed = {
    'max_session_id' : max_session_id,
    'data' : data,
    'up_to_date' : up_to_date,
    'removed' : removed_dict
}
with open("parsed.json","w") as fp:
    json.dump(parsed, fp, indent=4)

locs = {}

for k, entry in up_to_date.items():
    loc = entry['location']

    if loc not in locs:
        locs[loc] = 0
    
    locs[loc] =locs[loc]+1

locs = sorted([(x,y) for x,y in locs.items()], key=lambda x:x[1])
pprint.pprint(locs,width=160)

bob = {k:i for k,i in up_to_date.items() if i['location']=='Böblingen'}
pprint.pprint(bob)

keywords = {}
for k, entry in data.items():
    title = entry[-1]['title']
    title = title.replace(',',' ')
    title_words = title.split(' ')
    for word in title_words:
        word = word.strip('*in')
        word = word.strip(')')
        word = word.strip('(')
        
        if word in keywords:
            keywords[word] +=1
        else:
            keywords[word] = 1
BLACKLIST = {
    '',
    'm/w/d',
    'w/m/d',
    'w/m',
    'm/w',
    'f/m/d',
    'm/f/d',
    'm/w/x',
    'M/W/D',
    'm',
    'de',
    'für',
    '/',
    'im',
    '&',
    'als',
    '-',
    '–', # different char
    'in',
    'und',
    'die',
    'mit',
    '|',
    'oder',
    'and',
    'von',
    'of',
    'den',
    'bei',
    'zur',
    'der',
    'Schwerpunkt',
    'Bereich',
    'Project',
    'for'
}


keywords = {k:v for k,v in keywords.items() if k not in BLACKLIST}

SYNONYM = {
    'Software-Entwickler' : 'Softwareentwickler',
    'Architect' : 'Architekt'
}

for k, v in SYNONYM.items():
    if k in keywords:
        keywords[v]+= keywords[k]

keywords = {k:v for k,v in keywords.items() if k not in SYNONYM}


keyword_list = sorted([(x,y) for x,y in keywords.items()], key=lambda x:x[1])
pprint.pprint(keyword_list)

with open("keywords.txt","w") as fp:
    for l in keyword_list:
        fp.write("{}\n".format(l))
