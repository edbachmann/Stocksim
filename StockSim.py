
#Stock game simulator

import pandas as pd
import numpy as np
import string
import random
import sys

from classes_stocksim import round_object as rb
from classes_stocksim import round_update as ru
from classes_stocksim import stockinit as si

from tkinter import *
from tkinter import ttk


#build initial stock data

stock_data = si.init_stock_data()
industry_name = stock_data.loc["Industry"]
previous_round = stock_data.loc["Previous Round"]
current_round = stock_data.loc["Current Round"]
next_round = stock_data.loc["Next Round"]
corrtype = ["pos","neg","poly","random"]
stock_names = list(string.ascii_uppercase)
hidden_bias = []
biased_stock = []
param_set = False

#variables for game engine
liquid_cash = 123
shares_purchased = dict.fromkeys(stock_names,0)
roundNum = 1
dayNum = 1
Cor_type = " "
Cor_mag = 0
Cor_num = 0
Indust_boo = BooleanVar
round_update_obj = object

#create dict for current round stock look up
# to be called at end of round to update
# stock_price is used by the buy/sell funcs
def stockPrice():   
    stock_price = {}
    for count, key in enumerate(stock_names):
        stock_price[key] = current_round[count]
    return stock_price
stock_price = stockPrice()    


#create a list for purchased shares
#Used for testing the buy functions
#def displayShares():
#    display_shares = []
#    for key in shares_purchased:
#        if shares_purchased.get(key) > 0 :
#            display_shares.append("{}".format(shares_purchased.get(key),key))
#    return display_shares



########### Simulator UI


window = Tk()





#tkinter stuff idk
content = ttk.Frame(window)
frame = ttk.Frame(content, borderwidth=1, relief="ridge", width=900, height=900)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)
window.title("Stock Simulator 5000")
window.resizable(0, 0)
screenLine = "*" *300



#show game progression
roundLabel = str("Round {} of 39 \n Day {}".format(roundNum,dayNum))
lblRound = Label(window, text = roundLabel)
lblLine0 = Label(window, text = screenLine)


# create the stock display
#called to update stock display at end of every round
#display_shares = displayShares()

lblStocks = []
lblIndustrys= []
lblprev_rounds = []
lblcur_rounds = []
lblnxt_rounds = []


for i in range(26):

        lblStock = Label(window, text= list(string.ascii_uppercase)[i])
        lblStocks.append(lblStock)
       
        lblStocks[i].grid(row = 2, column= i, columnspan=3)
##
        lblIndustry = Label(window, text= industry_name[i])
        lblIndustrys.append(lblIndustry)
        
        lblIndustrys[i].grid(row = 3, column= i, columnspan=3)
##
        lblprev_round = Label(window, text= previous_round[i])
        lblprev_rounds.append(lblprev_round)
        
        lblprev_rounds[i].grid(row = 4, column= i, columnspan=3)
##
        lblcur_round = Label(window, text= current_round[i])
        lblcur_rounds.append(lblcur_round)
        
        lblcur_rounds[i].grid(row = 5, column= i, columnspan=3)    
##
        lblnxt_round = Label(window, text= next_round[i])
        lblnxt_rounds.append(lblnxt_round)

        lblnxt_rounds[i].grid(row = 6, column= i, columnspan=3)

       # if len(display_shares) >0:
       #     lblShares = Label(window, text= display_shares[i])
       #     lblShares.grid_columnconfigure(5)
       #     lblShares.grid(row = 7, column= i, columnspan=3,rowspan= 3,)    

#also called immediately to generate display
#dispStocks()


#updates labels in tkinter 
def shares_display_update():
    global lblStocks,lblIndustrys,lblprev_rounds,lblcur_rounds,lblnxt_rounds
    for i in range (26):

        lblprev_rounds[i]['text'] = previous_round[i]
        lblcur_rounds[i]['text'] = current_round[i]
        lblnxt_rounds[i]['text'] = next_round[i]



lblLine1 = Label(window, text = screenLine)
lblPortf = Label(window, text="Portfolio: ")
lblLine2 = Label(window, text = screenLine)
lblCash = Label(window, text = "Cash on hand: {}".format(liquid_cash))
#lblShares = Label(window, text = display_shares,wraplength= 500)




    

#  game log area

lblRound.grid(row=0, column=0, columnspan=26)

lblLine0.grid(row=1, column=0,columnspan=26)


lblLine1.grid(row=10, column=0, columnspan=26)
lblPortf.grid(row=11, column=0, columnspan=26) 
lblCash.grid(row=15, column=0, columnspan=26)
#lblShares.grid(row = 12, column= 0, columnspan= 26, rowspan= 3)
lblLine2.grid(row=16, column=0, columnspan=26)

# correlation selection menu
corrtype_ent = StringVar(window)
corrtype_ent.trace_add('write', lambda *args: corrtype_ent.get())

corrtype_OM = OptionMenu(window, corrtype_ent, *corrtype)

lblCorrEntry = Label(window, text="Correlation Type:")
corrtype_OM.grid(row=17, column=4, columnspan=2)
lblCorrEntry.grid(row=17, column=2, columnspan=2)
corrtype_ent.set(corrtype[0]) # default value

#corr magnitude menu
corrMag_ent = Entry(window)
corrMag_ent.insert(END,"10") # default value


lblCorrMagEntry = Label(window, text="Corr. Strength % :")
corrMag_ent.grid(row=18, column=4, columnspan=2)
lblCorrMagEntry.grid(row=18, column=2, columnspan=2)

# number of correlation relationships
lblCorrAmtEntry = Label(window, text="# Corr. Stocks").grid(row=17)
entCorrAmtEntry = Entry(window)
entCorrAmtEntry.grid(row=17, column=1, columnspan=1)
entCorrAmtEntry.insert(END,"2") # default value


# Industry toggle
lblIndustEntry = Label(window, text="Use Industry").grid(row=18)
entIndustEntry = ttk.Checkbutton(window,text="Use?", variable= Indust_boo)
entIndustEntry.grid(row=18, column=1, columnspan=1)

# number of correlation relationships
lblInitCashEntry = Label(window, text="Starting Cash").grid(row=17, column= 6,columnspan=2)
entInitCashEntry = Entry(window)
entInitCashEntry.grid(row=17, column=8, columnspan=2)
entInitCashEntry.insert(END,"10000") # default value

# set parameters for the simulator
btnSimpar = Button(window, text="Set Sim Parameters", command=lambda: simParmSet(corrtype_ent.get(),corrMag_ent.get(),entCorrAmtEntry.get(),entIndustEntry.instate(['selected']),entInitCashEntry.get()))



# parameters are explained in the print at the bottom of the function
def simParmSet(CorType,CorMag,CorNum,IndustBoo,initCash):
    global liquid_cash,lblCash,round_update_obj,param_set
    #Cor_mag,Cor_type,Cor_num,Indust_boo,hidden_bias,biased_stock
    param_set = True
    Cor_type = CorType
    Cor_mag = float(CorMag)
    
    #ensure correct number of correlated stocks 
    if  1 <= int(CorNum) <= 26:
        Cor_num = int(CorNum)
    else:
        Cor_num = 2
        print ("Stock correlation value must be between 2 and 25. \n Value set to 2 as default.")

    Indust_boo = IndustBoo
    liquid_cash = initCash
    lblCash['text'] = liquid_cash
    stock_names = list(string.ascii_uppercase)
    #print(stock_names)
    hidden_bias =  random.sample(stock_names,Cor_num + 1)
    biased_stock = random.sample(hidden_bias,1)

    biased_stock_enum = stock_names.index(biased_stock[0])

    
    
    #tmp = str(biased_stock[0])
    hidden_bias.remove(biased_stock[0])

    print("Parameters set. \n The type of correlation will be: {} \n \
         The magnitude of the correlation will be: {} \n \
         The number of correlated stocks will be:  {}    \n \
         Industry correlation = {} \n \
    The amount of starting cash will be {} \n \
        The independent stocks will be: {} \n \
        The stock that will be biased is {}"\
    .format(Cor_type,Cor_mag,Cor_num,Indust_boo,liquid_cash,hidden_bias,biased_stock))

    round_update_obj = rb.NextRoundobj(Cor_type,Cor_mag,Indust_boo,hidden_bias,biased_stock_enum,stock_data)





#sell button was for testing the orginal simulator but I am keeping it in
#btnSell = Button(window, text="Sell", command=lambda : sellStock(entCorrAmtEntry.get(),entAmtEntry.get()))

# next round button was also for initial testing 
btnNext = Button(window, text="Start", command=lambda : nextRound())

btnSimpar.grid(row=21, column=1, columnspan=1)
#btnSell.grid(row=21, column=2, columnspan=1)
btnNext.grid(row=21, column=13, columnspan=13)
#print(display_shares)
# Main game logic


def buyStock(stock,shares):
    global liquid_cash, lblCash,shares_purchased, display_shares, lblShares
    stock_cost= int(stock_price.get(stock)) * int(shares)
    
    print("{} shares of {} have been bought".format(shares,stock))
    print(stock_cost)
    # if statement was for testing but leaving it in in case of issue with ai inputs
    if stock_cost > liquid_cash:
        print("You are too poor")
    else:
        liquid_cash = liquid_cash - stock_cost
        lblCash['text'] = liquid_cash
        shares_purchased[stock] = int(shares) + int(shares_purchased[stock])
        
        #lblShares['text'] =shares_purchased




def sellStock(stock,shares):
    global liquid_cash, lblCash,shares_purchased, display_shares, lblShares
    stock_cost= int(stock_price.get(stock)) * int(shares)

    print("{} shares of {} have been sold".format(shares,stock))
    # same as the buy function, I am leaving this in for testing
    if int(shares) > int(shares_purchased[stock]):

        print("You don't own enough of that stock")
    else:
        liquid_cash = liquid_cash + int(stock_cost)
        lblCash['text'] = liquid_cash
        shares_purchased[stock] = int(shares_purchased[stock]) - int(shares)
        
       # lblShares['text'] =shares_purchased



def nextRound():
    global previous_round,current_round,next_round,stock_data,stock_price,roundNum,dayNum,roundLabel,lblRound
    print("Engaging Next Round..." )
    if not param_set:
        print("Parameters have not been initialized \n Round not changed")
    else:

        
        round_update_obj.CorrMotion()

                
        previous_round = round_update_obj.stock_df_previous
        current_round = round_update_obj.stock_df_current
        next_round = round_update_obj.stock_df_next
       
        
        stock_price = stockPrice()
        shares_display_update()

        if roundNum  < 39:
            roundNum += 1
        else:
            roundNum = 1
            dayNum +=1 
        roundLabel = str("Round {} of 39 \n Day {}".format(roundNum,dayNum))
        lblRound['text']=roundLabel
        #print(round_update_obj.Cor_type)




   
    




   
   





window.mainloop()