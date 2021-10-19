import random
import numpy as np
import string
import pandas as pd

def init_stock_data():

 stock_names = list(string.ascii_uppercase)
 stock_price_init = np.random.randint(10, 250, 26)
 industry_name = ["brick", "lumber", "wool", "grain", "ore"]
 industry_name = random.choices(industry_name, k=26)
 index_values =np.array(["Industry","Previous Round","Current Round","Next Round"])
 stock_price_init = np.array(stock_price_init)

 stock_data = pd.DataFrame(index=index_values,columns=stock_names)

 stock_data.loc["Industry"] = industry_name
 stock_data.loc["Previous Round"] = stock_price_init
 stock_data.loc["Current Round"] = stock_price_init
 stock_data.loc["Next Round"] = stock_price_init

 return stock_data

