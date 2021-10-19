#from classes_stocksim.hidden_bias import hidden_bias
import numpy as np
import random
import pandas as pd
import string


stock_names = list(string.ascii_uppercase)

def round_update(current):


        """
         hidden_bias = list of stocks whose movements will effect the biased stock
         biased_stock = stock that will be influenced, The stock we want our ai to identify 
         current_round = the current dataframe


        """

        df_next = []#list(next)
        df_current = list(current)
        movement = list(range(26))


#Generate random movements for each stock for the next round
        for i in range(0,26):
            movement[i] =round(np.random.uniform(low=-1, high=1),4) /10
        


        movement = np.array(movement)
       

        df_next = movement

     


        df_next = df_next * df_current
        df_next = df_current + df_next
        #df_next =pd.DataFrame(df_next,columns=stock_names)
        #print("Stock B started at {} and was multiplied by a movement of {} to equal {}".format(df_current[1],movement[1],df_next[1]))

###
# Zero out stocks that have crashed 
        for i in range(26):
             df_next[i] = round(df_next[i],2)
             if (df_next[i] < 1):
                 df_next[i] == 0

        
       
        return df_next


