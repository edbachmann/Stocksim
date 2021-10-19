import numpy as np
import random
import pandas as pd
import string
from .round_update import round_update 

# take simulator parameters to create the bias modifyers for round update
class NextRoundobj():
    def __init__(self,Cor_type,Cor_mag,Indust_boo,hidden_bias,biased_stock_enum,stock_df):

        self.Cor_type = Cor_type
        self.Cor_mag = (int(Cor_mag) / 100) + 1
        self.Indust_boo = Indust_boo
        self.hidden_bias = hidden_bias
        self.biased_stock = biased_stock_enum
        #self.lastround = []
        #self.currentround = []
        #self.nextround = []
        self.stock_df_previous = stock_df.loc["Previous Round"]
        self.stock_df_current = stock_df.loc["Current Round"]
        self.stock_df_next = stock_df.loc["Next Round"]
        
        
        


    def CorrMotion(self):

        self.stock_df_previous = self.stock_df_current
        
        self.stock_df_current = self.stock_df_next
        
        new_round = round_update(self.stock_df_current)
        
        

        movement_delta = {}
        total_movement = 0

   
        for count, stock in enumerate(self.hidden_bias):


                delta =  self.stock_df_current[self.hidden_bias.index(stock)] -self.stock_df_previous[self.hidden_bias.index(stock)]
                movement_delta[count] = delta / self.stock_df_current[self.hidden_bias.index(stock)] 

                if self.Cor_type == "pos":
                    movement_delta[count] = movement_delta[count] * self.Cor_mag
                if  self.Cor_type == "neg":
                    movement_delta[count] = movement_delta[count] * self.Cor_mag * -1
                if self.Cor_type == "poly":
                    x = float(movement_delta[count])
                    y = float(self.Cor_mag )
                    movement_delta[count] = 3*x*y**3 - 2*x*y**2 + x*y

                if self.Cor_type == "random":
                    print("What were you expecting?")
               
               
                total_movement = total_movement +  movement_delta[count]


        

        
        self.stock_df_next = new_round

        new_stock = self.stock_df_next[self.biased_stock] * (1 + round(total_movement,2))
        #print("{} multiplied by {} equals {}".format(self.stock_df_next[self.biased_stock],total_movement,new_stock))


        if new_stock <= 1:
            new_stock = 0
        self.stock_df_next[self.biased_stock] = round(new_stock,2)


    

