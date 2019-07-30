# pylint: disable=too-many-function-args
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import json

def load_data():

    with open('stocks/ADIDAS AG.json') as fp:
        data = json.load(fp)

    meta = data['META']
    dt = np.dtype([
        ('date', 'object'),
        ('opening', 'f4'),
        ('high', 'f4'),
        ('low', 'f4'),
        ('closing', 'f4'),
        ('volume', 'i4')
    ])
    
    quotes = np.array([tuple(r) for r in data['QUOTES']], dtype=dt)
    print(quotes['date'])
    return meta, quotes