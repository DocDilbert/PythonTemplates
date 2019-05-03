import json
import pprint
with open("ss.json", encoding="utf-8") as fp:
    data = json.load(fp)


locs = {}

for entry in data:
    loc = entry['location']

    if loc not in locs:
        locs[loc] = 0
    
    locs[loc] =locs[loc]+1

locs = sorted([(y,x) for x,y in locs.items()], key=lambda x:x[0])
pprint.pprint(locs,width=140)

with open("locs.json","w") as fp:
    json.dump(locs, fp, indent=4)