# pylint: disable=too-many-function-args
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt


def main():
    dates = np.genfromtxt('daimler.csv', delimiter=',',
                          dtype='datetime64', usecols=[0])
    prices = np.genfromtxt('daimler.csv', delimiter=',',
                           dtype='float64', usecols=[1, 2, 3, 4])
    a = np.genfromtxt('daimler.csv', delimiter=',',
                      dtype='float64', usecols=[1])
    volume = np.genfromtxt('daimler.csv', delimiter=',',
                           dtype='int', usecols=[5])

    
    np.printoptions(edgeitems=5)
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
