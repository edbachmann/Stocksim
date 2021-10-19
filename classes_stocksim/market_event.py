import random
import numpy as np

#Simulates market factors changing industry wide
# Still not sure when to call or however strong the effect needs to be
#needs expermintation 

def market_events():

    markets = {
     "brick" : 0,
     "lumber" :0,
     "wool" : 0,
     "grain" : 0,
     "ore" : 0
     }  

    industryfactor = ["brick", "lumber", "wool", "grain", "ore"]
    industryfactor.extend(["none" for i in range(5)])
    industryfactor= random.choices(industryfactor, k= 2)


    for key in industryfactor:
        markets[key] = round(np.random.uniform(low=-1, high=1),2)

    
        
    
    return markets




