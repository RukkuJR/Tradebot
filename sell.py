from exchange_python.client import Client as exchange
import os
import time
import requests
import json
from twilio.rest import Client as twilio
from datetime import date

#Withdraw
#XXXX
#XXX
#XX
 
 
#######How to Run this script & Procss##########
####step 2: create a day api to trade from exchange website. copy paste here
####step 3: Decide on min chunk to sell and how much to trade in total/auto. Enter in the declare variable in this script
####step 4: execute script
####step 5: check trade stats in exchange web
####step 6: disable api


##########Constant###########
maker_fee = 0.0025
taker_fee = 0.005
acnt_id = 7403405207174367813
spread_act = 3
minsellamt = 32    #these may not be relevant
total_trade = 32.0        #these may not be relevant
today = date.today()

###########Declare Variables######################
currency = 'XBT'    #to check balance - LTC-litecoin, ETH - etherium, XRP- Ripple, XBT- crypto, MYR-RM - 
trade_pair = 'XBTMYR'     #LTCMYR , ETHMYR, XRPMYR, XBTMYR  -- to trade
#last_bought = 32#last_bought = 3000 #how much money did you bought last time?No Need
auto_manual = 0     #1= auto, 0=manual
btc_to_sell = 0.0005 #######this is the important factor


f = open("xxx\\last_purchase_price.txt", "r")
last_purchase_price = float(f.readline())
f.close()

f = open("xxx\\last_purchase_volume.txt", "r")
last_purchase_volume = float(f.readline())
f.close()


c = exchange(api_key_id='xxx', api_key_secret='xxx')
try:

##############getlatestbalance#########################################
    res = c.get_balances(assets=[currency]) 
    account_obj = str(res)
    account_obj = account_obj.replace("\'", "\"")
    account_json  = json.loads(account_obj)
    mybal = account_json['balance'][0]['balance']
    mybal = float(mybal)  #this coin balance just for reference
    max_no_order = total_trade/minsellamt     #No of times i can put orders 
    res = c.get_fee_info(trade_pair)
    print(res) 
    print("I have ",mybal,"balance in my exchange account")
    #print("number of times I can put automatatic sell order = ",max_no_order)
    
    #condition to make sure you want loop for trading / do one time trading
    if auto_manual == 0:
        max_no_order = 1.5
        print("Max_no_of_order = ",max_no_order)
    else:
        a =1


    while  max_no_order > 1:
    
        print("trade undergoing and remaining is ",max_no_order)
        
        ticker = c.get_ticker(pair=trade_pair)
        last_bid = float(ticker["bid"])
        last_ask = float(ticker["ask"])
        last_trade = float(ticker["last_trade"])
        spread_act = last_ask - last_bid
        print("Spread at moment is ",spread_act)
        print(ticker)
        print("last purchase price when i bought crypto was 1 crypto = ",last_purchase_price)
        
            
        ####how much BTC volume & and what price willing to sell######

        my_ask_rate = last_ask - 1 ##########to ensure buyers take my bid first or trigger
        stop_ask_rate = my_ask_rate - 10 ######maximum i can turun harga
        #btc_to_sell =   round((last_bought/last_purchase_price),6) ####I just want to sell what i bought last time but with diffrent rate
        #btc_to_sell = round(((1/my_ask_rate) * minsellamt),6)  #max can have 6 decimal only
        
        print("current market rate of  crypto was 1 crypto = ",stop_ask_rate)
        growth = round((((stop_ask_rate - last_purchase_price) / last_purchase_price) * 100),2)
        print("The yield if I sell now is  = ",growth,"%")

        account_sid = 'xxx' 
        auth_token = 'xxx' 
        client = twilio(account_sid, auth_token) 
        if growth <= 2.5:         
            message = client.messages.create( 
                              from_='whatsapp:+14xxx',  
                              body='Your crypto sell order of 0.0005 has failed becuase growth less than 2.5% on 2019. Details: hodling crypto else you decide to stop trade',                              
                              to='whatsapp:+601xxx' 
                          ) 
            print(message.sid);
            
            #####write status of last sell
            f = open("xxx\\sell_status.txt", "a")
            f.write(str(today))
            f.write("Your crypto sell order of 0.0005 has failed becuase growth less than 2.5% . hodling crypto else you decide to stop trade ")
            f.close()
            
        else:
            message = client.messages.create( 
                              from_='whatsapp:+141xxx',  
                              body='Your crypto sell order of 0.0005 was succesful congrats becuase growth more than 2.5% on 2019. Details: Check crypto news',
                              to='whatsapp:+6016xxx' 
                          ) 
            print(message.sid);
            
            #####write status of last sell
            f = open("xxx\\sell_status.txt", "a")
            f.write(str(today))
            f.write("Your crypto sell order of 0.0005 was succesful congrats becuase growth more than 2.5% today. ")
            f.close()
            ##############limit_order_not working--maybe with money may work#########################################  
            limit_order = c.post_limit_order(trade_pair, type = 'ASK', volume = btc_to_sell, price = stop_ask_rate, stop_price = my_ask_rate, stop_direction= 'BELOW' , base_account_id=None,counter_account_id=None)
           #############################################################
            a =1

        max_no_order -= 1
  
except Exception as e:
  print(e)
  
