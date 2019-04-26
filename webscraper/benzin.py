import matplotlib.pyplot as plt
import re
from datetime import datetime

UUIDS = {}
RDATE = re.compile("(\d+\.\d+\.\d+),\s(\d+:\d+)")

def parse_line(line):
    elements = line.split(";")
    session_id = int(elements[0])
    uuid = elements[1].strip("\"")
    headline = elements[2].strip("\"")
    adr = elements[3].strip("\"")
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

    pricelist.append((session_id, dt, price, adr)) 
def remove_identicial_rows(li):
    
    iresult = {i[1] : i for i in li}
    reduced_list = [iresult[k] for k in sorted(iresult.keys())]
    return reduced_list
def main():
    with open('out.csv','r', encoding='utf8') as fp:
        line = fp.readline()
        
        while line:
            parse_line(line)
            line = fp.readline()
    
    for _, uuid in UUIDS.items():
        for product, pricelist in uuid.items():
            reduced_list = remove_identicial_rows(pricelist)
            uuid[product] = reduced_list

    
    plt.figure(figsize=(50, 50)) # This increases resolution
    plt.subplots_adjust(left=0.01,right=0.99,top=0.99, bottom=0.01, wspace = 0.15)
    cnt = 1
    min_price = 10000
    max_price = 0
    for uuid,productdict in UUIDS.items():
        pricelist = productdict['Super (E10) Benzin']
        prices = [i[2] for i in pricelist]
        min_price = min(min_price, min(prices))
        max_price = max(max_price, max(prices))

    for uuid,productdict in UUIDS.items():
        pricelist = productdict['Super (E10) Benzin']
        x = [(i[1].timestamp()-datetime.now().timestamp())/(60*60*24) for i in pricelist]
        y = [i[2] for i in pricelist]
        title = pricelist[0][3]
        axarr = plt.subplot(9,8, cnt)
        axarr.xaxis.set_visible(False) # Hide only x axis
        plt.step(x,y,'-')
        plt.title(title)
        plt.ylim([min_price*0.99, max_price*1.01])
        cnt +=1
        if cnt>9*8:
            break
    
    plt.savefig('foo.png')
 
if __name__ == "__main__":
    main()