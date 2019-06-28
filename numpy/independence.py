
import math
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import *
import matplotlib.pyplot as plt


def get_age(birthday):
    first_day = birthday 
    last_day  = date.today() 

    td = relativedelta(last_day, first_day)

    return ((td.years*12.0 + td.months)/12.0)

def whole_monthes_to_age(age, birthday):
    birthday_at_age = relativedelta(years=age)+birthday

    now =  datetime.now()

    #now = date(2019,10,10)
    first_day = now +  relativedelta(
        hour=23, 
        minute = 59, 
        second=59, 
        day=1, 
        months=1, 
        days=-1
    ) 
    last_day  = birthday_at_age +  relativedelta(day=1) 
    rd = relativedelta(last_day, first_day)
    return(rd.months + rd.years*12)

def calc_mpr(apr):
    """ Calculates the monthly percentage yield (mpr) from the annual percentage yield (apr)
    
    Arguments:
        apr  -- annual percentage yield
    Returns:
        mpr -- monthly percentage yield
    """
    return (math.pow(1.0+apr/100.0, 1.0/12.0)-1.0)*100.0

def get_my(ic, apr):
    """ Returns the monthly yield (my) from savings on a account

        ic -- initial_capital
        apr -- annual percentage yield
    """

    mpr = calc_mpr(apr)
    return ic  * mpr/100.0
    
def capital_over_month(to_month, ic, sr,  apr):
    """ Returns a DataFrame with the following content
            (start_c, my, ml, end_c)

            start_c -- Capital at start of month
            my      -- monthly yield
            end_c   -- Capital at end of month

    Arguments:
        to_month -- how many monthes should be calculated
        ic       -- initial capital
        sr       -- savings rate
        apr      -- anual percentage yield
    """
    re = []
    re.append((0.0, ic, get_my(ic, apr),  ic + get_my(ic, apr) ))
    
    for m in range(1, to_month+1):
        end_c_last = re[-1][-1]

        if callable(sr):
            start_c = sr(m)  + end_c_last
        else:
            start_c = sr  + end_c_last

        if start_c < 0.0:
            start_c = 0.0

        my = get_my(start_c, apr)

        end_c  = start_c + my
        year = m / 12.0
        re.append((year, start_c, my, end_c))
   
    ps = pd.DataFrame(re, columns=['year','start_c', 'my', 'end_c'])
    
    return ps


def savings_model(m, sr, lr, srapi, withdrawal_at_month):
    """ Returns the savings rate of a month width index m
    
    Arguments:
        m -- number of month
    
    Returns:
        Savings rate
    """
    if m >= withdrawal_at_month:
        return -lr
    else:
        cycle = math.floor(m/12.0)
        return sr *math.pow(1.0+srapi/100,cycle)


if __name__ == "__main__":
    #srapi -- savings rate annual percentage increase/decrease

    ic = 82000.0
    sr = 1360.0
    lr = 2000.0
    srapi = 11.9339641731106
    apr = 4.0

    
    monthes_50  = whole_monthes_to_age(50, date(1979,12,11))
    monthes_100 = whole_monthes_to_age(100, date(1979,12,11))

    print(type(savings_model))
    
    com = capital_over_month(
        monthes_100, 
        ic, 
        lambda m : savings_model(m, sr, lr, srapi, monthes_50), 
        apr
    )
    print(com.round(2))
    age = get_age(date(1979,12,11))
    plt.plot(age+com['year'], com['my'])
    plt.show()

    