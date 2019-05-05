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
