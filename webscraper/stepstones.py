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
    'm|w|d',
    'f/m',
    '[m/w/d]',
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
    'schwerpunkt',
    'mitarbeiter',
    'bereich',
    'project',
    'for',
    'i',
    'the',
    'all',
    "center",
    "amg",
    "stuttgart"
}

SYNONYM = {
    'architect' : 'architekt',
    "systeme" : "system",
    'softwarearchitect' : 'softwarearchitekt'
}

def build_keywords(text):
    keywords = {}
    text = text.replace(',',' ')
    text = text.replace('-',' ')
    text_words = text.split(' ')
    for word in text_words:
        word = word.replace('*in','')
        word = word.replace('/in','')
        word = word.strip(')')
        word = word.strip('(')
        word = word.lower()
        if word in SYNONYM:
            word = SYNONYM[word]

        if word not in BLACKLIST:
            if word in keywords:
                keywords[word] +=1
            else:
                keywords[word] = 1
    return keywords

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
 



locs = {}

for k, entry in data[max_session_id].items():
    loc = entry['location']

    if loc not in locs:
        locs[loc] = 0
    
    locs[loc] =locs[loc]+1

locs = sorted([(x,y) for x,y in locs.items()], key=lambda x:x[1])
#pprint.pprint(locs,width=160)

keywords = {}
for _, dataset in data.items():
    for _, entry in dataset.items():
        title = entry['title']
        title_keywords = build_keywords(title)

        for word, count in title_keywords.items():
            if word in keywords:
                keywords[word] += count
            else:
                keywords[word] = count

keyword_sum = sum(count for _, count in keywords.items())
keywords = sorted([{
    'keyword':x,
    'occurrences':y, 
    'relevance':round(y/keyword_sum*100,3)
} for x,y in keywords.items()], key=lambda x:x['occurrences'])


#pprint.pprint(keywords)

RELEVANCE_THRESHOLD = 0.1 #%

important_keywords = [ k
    for k in keywords
    if k['relevance'] > RELEVANCE_THRESHOLD
]

keyword_set = { k['keyword'] for k in important_keywords}

for _, dataset in data.items():
    for _, entry in dataset.items():
        entry['keywords'] = [k for k,_ in build_keywords(entry['title']).items() if k in keyword_set]

parsed = {
    'max_session_id' : max_session_id,
    'keywords' : important_keywords,
    'data' : data
}
with open("stepstones.json","w") as fp:
    json.dump(parsed, fp, indent=4)


with open("keywords.txt","w",encoding="utf-8") as fp:
    for l in keywords:
        fp.write("{}\n".format(l))

with open("irrelevant.txt","w",encoding="utf-8") as fp:
    for k, d in data[max_session_id].items():
        if len(d['keywords'])==0:
            fp.write("{} {}\n".format(k, d['title']))