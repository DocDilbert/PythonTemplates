import matplotlib.pyplot as plt
import re
import pickle
from datetime import datetime

    
def main():
    print("Reading Pickle ...")
    with open('data.pickle', 'rb') as outfile:  
        UUIDS=pickle.load(outfile)

    print("Plotting data...")
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

    for uuid, productdict in UUIDS.items():
        print("-> Plotting data with uuid {}".format(uuid))
        pricelist = productdict['Super (E10) Benzin']
        x = [(i[1].timestamp()-datetime.now().timestamp())/(60*60*24) for i in pricelist]
        y = [i[2] for i in pricelist]
        title = pricelist[0][3]
        axarr = plt.subplot(9,9, cnt)
        axarr.xaxis.set_visible(False) # Hide only x axis
        plt.step(x,y,'-')
        plt.title(title)
        plt.ylim([min_price-0.001, max_price+0.001])
        cnt +=1
        if cnt>9*9:
            break
    
    print("Saving Plot...")
    plt.savefig('foo.png')
 
if __name__ == "__main__":
    main()