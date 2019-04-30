import matplotlib.pyplot as plt
import re
import pickle
from datetime import datetime

    
def main():
    print("Reading Pickle ...")
    with open('data.pickle', 'rb') as outfile:  
        data=pickle.load(outfile)

    print("Plotting data...")
    plt.figure(figsize=(50, 50)) # This increases resolution
    plt.subplots_adjust(left=0.01,right=0.99,top=0.99, bottom=0.01, wspace = 0.11)
    cnt = 1
    min_price = 10000
    max_price = 0

    
    for uuid, item in data.items():
        pricelist = item['products']['Super (E10) Benzin']
        prices = [i['price'] for i in pricelist]
        min_price = min(min_price, min(prices))
        max_price = max(max_price, max(prices))

    for uuid, item in data.items():
        print("-> Plotting data with uuid {}".format(uuid))
        pricelist = item['products']['Super (E10) Benzin']
        x = [(i['timestamp'].timestamp()-datetime.now().timestamp())/(60*60*24) for i in pricelist]
        y = [i['price'] for i in pricelist]
        title = item['headlines'][0]['headline']
        axarr = plt.subplot(9,9, cnt)
        axarr.xaxis.set_visible(False) # Hide only x axis
        plt.step(x,y,'-')
        plt.title(title)
        plt.ylim([min_price-0.001, max_price+0.001])
        cnt +=1
        if cnt>9*9:
            break
    
    print("Saving Plot...")
    plt.savefig('gas_stations.png')
 
if __name__ == "__main__":
    main()