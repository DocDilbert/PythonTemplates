import matplotlib.pyplot as plt
import re
import pickle
import pprint
from datetime import datetime

GAS_STATIONS = {}
REGEX_DATE = re.compile(r"(\d+\.\d+\.\d+),\s(\d+:\d+)")


def parse_line(line):
    elements = line.split(";")
    session_id = int(elements[0])
    uuid = elements[1].strip("\"")
    headline = elements[2].strip("\"")
    adr = elements[3].strip("\"").split("#?#")
    price = float(elements[4].strip("\"").strip("€").replace(",", "."))
    product = elements[5].strip("\"")
    timel = elements[7].strip("\"")
    rege = REGEX_DATE.search(timel)
    date_ = rege.group(1)
    time_ = rege.group(2)
    dt = datetime.strptime(date_+" "+time_, '%d.%m.%Y %H:%M')
    #print(session_id,uuid, product, dt)

    if uuid not in GAS_STATIONS:
        GAS_STATIONS[uuid] = {}

    gas_station = GAS_STATIONS[uuid]

    if product not in gas_station:
        gas_station[product] = []

    pricelist = gas_station[product]

    pricelist.append((
        session_id,
        dt,
        price,
        headline,
        adr,
    ))


def remove_identicial_rows(li):

    # compare whole dataset
    iresult = {str(i[1])+str(i[2])+str(i[3])+" ".join(i[4]): i for i in li}
    reduced_list = [iresult[k] for k in sorted(iresult.keys())]

    #for k,_ in iresult.items():
    #    print(k)
    return reduced_list


def main():
    print("Reading file ...")
    with open('out.csv', 'r', encoding='utf8') as fp:
        line = fp.readline()

        while line:
            parse_line(line)
            line = fp.readline()

    for _, gas_stations in GAS_STATIONS.items():
        for product, pricelist in gas_stations.items():
            reduced_list = remove_identicial_rows(pricelist)
            gas_stations[product] = reduced_list

    print("Writing Pickle ...")
    with open('data.pickle', 'wb') as outfile:
        pickle.dump(GAS_STATIONS, outfile)

    pprint.pprint(GAS_STATIONS)


if __name__ == "__main__":
    main()
