import json
import pprint
with open("ss.json", encoding="utf-8") as fp:
    data = json.load(fp)

uuid_dict = {}
for entry in reversed(data):
    uuid = entry['uuid']
    entry.pop('uuid',None) # remove uuid
    entry_without_id= dict(entry)
    entry_without_id.pop('session_id', None)
    if uuid in uuid_dict:
        last = uuid_dict[uuid][-1]
        last_without_id = dict(last)
        last_without_id.pop('session_id', None)

        if last_without_id != entry_without_id:
            uuid_dict[uuid].append(entry)
    else:
        uuid_dict[uuid]= []
        uuid_dict[uuid].append(entry)

for key, _ in uuid_dict.items():
    uuid_dict[key]=list(reversed(uuid_dict[key]))

with open("parsed.json","w") as fp:
    json.dump(uuid_dict, fp, indent=4)
