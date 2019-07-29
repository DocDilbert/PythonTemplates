# pylint: disable=too-many-function-args
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import json

def main():

    with open('daimler.json') as fp:
        data = json.load(fp)

    quotes = np.array(data['QUOTES'])
   
    dates = np.array(quotes[:,0], dtype='datetime64')
    _prices = np.array(quotes[:,1:4], dtype='float64')
    a = np.array(quotes[:,1],dtype='float64')
    _volume = np.array(quotes[:,5],dtype='int')


    min_date = np.min(dates)
    days = (dates-min_date)
    max_days = np.max(days) / np.timedelta64(1, 'D')
    print(days.size)
   
    days_ip = np.arange(0, max_days+1)
    days = days / np.timedelta64(1, 'D')
    print(days_ip)
    print(days)
    print(a)

    closing_ip = np.interp(days_ip, days, a)
    dates_ip = min_date + [np.timedelta64(int(x), 'D') for x in days_ip]
    plt.plot(dates_ip, closing_ip)
    plt.show()


if __name__ == "__main__":
    main()
