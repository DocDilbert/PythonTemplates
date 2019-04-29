import matplotlib.pyplot as plt
import re
import pickle
import pprint
from datetime import datetime

UUIDS = {}
RDATE = re.compile(r"(\d+\.\d+\.\d+),\s(\d+:\d+)")

def parse_line(line):
    elements = line.split(";")
    session_id = int(elements[0])
    uuid = elements[1].strip("\"")
    headline = elements[2].strip("\"")
    adr = elements[3].strip("\"").split("#?#")
    price = float(elements[4].strip("\"").strip("€").replace(",","."))
    product = elements[5].strip("\"")
    timel = elements[7].strip("\"")
    rege=RDATE.search(timel)
    date_ = rege.group(1)
    time_ = rege.group(2)
    dt = datetime.strptime(date_+" "+time_, '%d.%m.%Y %H:%M')
    #print(session_id,uuid, product, dt)

    if uuid not in UUIDS:
        UUIDS[uuid] = {}
    
    products = UUIDS[uuid]

    if product not in products:
        products[product] = []

    pricelist = products[product]

    pricelist.append((
        session_id, 
        dt, 
        price, 
        headline,
        adr,
    )) 

def remove_identicial_rows(li):
    
    iresult = {i[1] : i for i in li}
    reduced_list = [iresult[k] for k in sorted(iresult.keys())]
    return reduced_list

    
def main():
    print("Reading file...")
    with open('out.csv','r', encoding='utf8') as fp:
        line = fp.readline()
        
        while line:
            parse_line(line)
            line = fp.readline()

    for _, uuid in UUIDS.items():
        for product, pricelist in uuid.items():
            reduced_list = remove_identicial_rows(pricelist)
            uuid[product] = reduced_list

    print("Writing Pickle ...")
    with open('data.pickle', 'wb') as outfile:  
        pickle.dump(UUIDS, outfile)
 
    pprint.pprint(UUIDS)
if __name__ == "__main__":
    main()