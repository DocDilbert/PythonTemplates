import json
import pprint
with open("stepstones_raw.json", encoding="utf-8") as fp:
    raw_data = json.load(fp)

BLACKLIST = {
    '',
    'm/w/d',
    'w/m/d',
    'w/m',
    'm/w',
    'f/m/d',
    'f/m/x',
    'm/f/d',
    'w/m/x',
    'm/w/x',
    'M/W/D',
    'm|w|d',
    'f/m',
    'm/w/divers',
    'für',
    '/',
    'im',
    '&',
    '•',
    'als',
    '-',
    '–', # different char
    'in',
    'und',
    'die',
    'das',
    'der',
    'des',
    'mit',
    '|',
    'oder',
    'and',
    'von',
    'of',
    'den',
    'bei',
    'zur',
    'unter',
    'Schwerpunkt',
    'Bereich',
    'Project',
    'for',
    'I',
    'the',
    'all'
}

SYNONYM = {
    'Software-Entwickler' : 'Softwareentwickler',
    'Architect' : 'Architekt'
}


data = {}
for session_id, entry in raw_data.items():
    if session_id not in data:
        data[session_id] = {}

    for i in entry:
        uuid = i['uuid']
        i.pop('uuid', None)

        if uuid in data[session_id]:
            # when the list changes during readout this can happen
            # always use the first element and discard the second, third, ...
            pass
        else:
            data[session_id][uuid] = i

max_session_id = max((
    sid for sid in data.keys()
))


# removed = {
#     k:i[-1] for k, i in data.items() if i[-1]['session_id']!=max_session_id
# }

# removed_dict = {}

# for key, entry in removed.items():
#     session_id = entry['session_id']
#     entry_copy = dict(entry)
#     entry_copy.pop('session_id', None)
#     if session_id in removed_dict:
#         removed_dict[session_id].update({key:entry_copy})
#     else:
#         removed_dict[session_id] = {}
#         removed_dict[session_id].update({key:entry_copy})
 


up_to_date = {
    k:i for k, i in data[max_session_id].items() 
}

parsed = {
    'max_session_id' : max_session_id,
    'data' : data,
    'up_to_date' : up_to_date,
}
with open("stepstones.json","w") as fp:
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
for _, dataset in data.items():
    for _, entry in dataset.items():
        title = entry['title']
        title = title.replace(',',' ')
        title_words = title.split(' ')
        for word in title_words:
            word = word.replace('*in','')
            word = word.strip(')')
            word = word.strip('(')
            
            if word in SYNONYM:
                word = SYNONYM[word]

            if word not in BLACKLIST:
                if word in keywords:
                    keywords[word] +=1
                else:
                    keywords[word] = 1


keywords = sorted([(x,y) for x,y in keywords.items()], key=lambda x:x[1])


with open("keywords.txt","w",encoding="utf-8") as fp:
    for l in keywords:
        fp.write("{}\n".format(l))


pprint.pprint(keywords)
