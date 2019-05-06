import matplotlib.pyplot as plt
import re
import pickle
import pprint
from datetime import datetime

REGEX_DATE = re.compile(r"(\d+\.\d+\.\d+),\s(\d+:\d+)")


def parse_line(line):
    elements = line.split(";")
    session_id = int(elements[0])
    uuid = elements[1].strip("\"")
    headline = elements[2].strip("\"")
    adr = elements[3].strip("\"").split("\\n")
    price = float(elements[4].strip("\"").strip("€").replace(",", "."))
    product = elements[5].strip("\"")
    timel = elements[7].strip("\"")
    rege = REGEX_DATE.search(timel)
    date_ = rege.group(1)
    time_ = rege.group(2)
    timestamp = datetime.strptime(date_+" "+time_, '%d.%m.%Y %H:%M')
    opening_time = elements[8].strip("\"").split("\\n")
    return {
        'uuid' : uuid,
        'session_id' : session_id,
        'timestamp' : timestamp,
        'price' : price,
        'product' : product,
        'headline' :headline,
        'adresses' : adr,
        'opening_time' : opening_time
    }



def build_price_list(data, uuid, product):

    li=[
        {
            'session_id' : i['session_id'],
            'timestamp' : i['timestamp'],
            'price' : i['price'],
        }
        for i in data
        if i['product'] == product and 
           i['uuid'] == uuid 
    ]

    # remove identical rows
    iresult = {
        (str(i['timestamp'])+str(i['price'])): i 
        for i in reversed(li)
    }
    return sorted([iresult[k] for k in sorted(iresult.keys())], key=lambda i : i['session_id'])

def build_one_feature_list(data, uuid, feature_name):

    li=[
        {
            'session_id' : i['session_id'],
            feature_name : i[feature_name]
        }
        for i in data
        if i['uuid'] == uuid 
    ]

    # remove identical rows
    iresult = {
        (str(i[feature_name])): i 
        for i in reversed(li)
    }
    return sorted([iresult[k] for k in sorted(iresult.keys())], key=lambda i : i['session_id'])

def build_product_list(data, uuid):
    products = set()

    for i in data:
        products.add( i['product'])

    product_list={
        i : build_price_list(data, uuid,  i)
        for i in products
    }
    return product_list

def build(data):
    stations = set()

    for i in data:
        stations.add(i['uuid'])

    station_list={
        i :  {
            'products' : build_product_list(data, i),
            'headlines' : build_one_feature_list(data, i, 'headline'),
            'adresses' : build_one_feature_list(data, i, 'adresses'),
            'opening_times' : build_one_feature_list(data, i, 'opening_time')
        }
        for i in stations
    }

    return station_list

def main():
    print("Reading file ...")
    data = []
    with open('out.csv', 'r', encoding='utf8') as fp:
        line = fp.readline().strip('\n')

        while line:
            data.append(parse_line(line))
            line = fp.readline().strip('\n')

    gas_stations = build(data)
    print("Writing Pickle ...")
    with open('data.pickle', 'wb') as outfile:
        pickle.dump(gas_stations, outfile)

    pprint.pprint(gas_stations,width=120)


if __name__ == "__main__":
    main()
