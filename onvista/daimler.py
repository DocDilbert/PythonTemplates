import numpy as np
import matplotlib.pyplot as plt
dates = np.genfromtxt('daimler.csv', delimiter=',', dtype='datetime64', usecols=[0])
prices = np.genfromtxt('daimler.csv', delimiter=',', dtype='float', usecols=[1,2,3,4])
volume = np.genfromtxt('daimler.csv', delimiter=',', dtype='int', usecols=[5])
print(repr(dates))
print(repr(prices))
print(repr(volume))


fig, ax = plt.subplots()
#eekFormatter = DateFormatter('%b %d, %Y')
#ax.xaxis.set_major_formatter(weekFormatter)
plt.plot(dates,prices)
plt.tight_layout()

plt.show()

