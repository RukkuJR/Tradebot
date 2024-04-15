#!/usr/bin/python

#######How to Run this script & Procss##########
####step 1: check price trend increasing over a week/month to decide whcryptoer to trade else don't look this script
####step 2: create a day api to trade from exchange website. copy paste here
####step 3: Decide on min chunk to purchas and how much to trade in total/auto. Enter in the declare variable in this script
####step 4: execute script & change spread if needed
####step 5: check trade stats in exchange web
####step 6: disable api

from exchange_python.client import Client as exchange
import os
import time
import requests
import json
import sys
from twilio.rest import Client as twilio
from datetime import date

##########Constant###########
maker_fee = 0.0025
taker_fee = 0.005
bid_accnt_id = XXX
spread_act = 3
min_btc_to_buy = 0.0005 ###exchange specific...can be rm 25/30/40 based on market price
today = date.today()

###########Declare Variables######################
currency = 'MYR'    #to check balance - LTC-litecoin, crypto - cryptoerium, crypto- Ripple, XBT- crypto, MYR-RM - 
trade_pair = 'XBTMYR'     #LTCMYR , cryptoMYR, cryptoMYR, XBTMYR  -- to trade
volatility_check = 0 #default(1) must not be volatile but if your are in rush its fine to make it volatile meaning spread can be 10000 for eg, let buyers decide to keep spread or not. 
minpurchase = 35 #minpurchase = 3000   #min must buy from exchange one time also how small i want to break the trade chunk
auto_manual = 0     #1= auto, 0=manual
cnd_auto_manual = 1 # 0 defualt whenever auto trade till the end of all available balance , 1= conditional auto manual trade.eg. have 1000 but only 500 need to buy,
cnd_mybal = 35 #cnd_mybal = 3000        #if you need autmated trading with min chunks and limit maximum aomount to trade. eg max RM 300 only to trade...otherwise this part no use
 ################please comment btc_toBuy in bleow script if you dont wish to buy min crypto. otherwise uncomment and topup rquired money 

c = exchange(api_key_id='XXXX', api_key_secret='XXX')
try:

    if trade_pair == 'cryptoMYR':
        precission = 2
    else:
        precission = 6

##############getlatestbalance#########################################
    res = c.get_balances(assets=[currency]) 
    account_obj = str(res)
    account_obj = account_obj.replace("\'", "\"")
    account_json  = json.loads(account_obj)
    mybal = account_json['balance'][0]['balance']
    mybal = float(mybal)
    max_no_order = mybal/minpurchase     #No of times i can put orders
    res = c.get_fee_info(trade_pair)
    print(res)    
    print("I have ",mybal,"balance in my exchange account")
    print("number of times I can put automatatic bid order = ",max_no_order)
    
    #condition to make sure you want loop for trading / do one time trading
    if auto_manual == 0:
        max_no_order = 1.5
        print("Max_no_of_order = ",max_no_order)
    elif auto_manual ==1 and  cnd_auto_manual == 1:
        max_no_order = cnd_mybal/minpurchase    
    else:
        a =1

    #time.sleep(3)
    # res = c.list_orders()
    #print(res)
    
   
    while  max_no_order > 1:
        if volatility_check == 1:   # Below is condition if youre willing to trade in a highly volatile spread market or not. Vice versa you have limit order and hence safe
            print("trade undergoing and remaining is ",max_no_order)
        
            #this below will put script on hold till have no rate inflation & market rate where seller and buyer ask same
            while  spread_act > 2:      
                ticker = c.get_ticker(pair=trade_pair)
                last_bid = float(ticker["bid"])
                last_ask = float(ticker["ask"])
                last_trade = float(ticker["last_trade"])
                spread_act = last_ask - last_bid
                print("Spread at moment is ",spread_act)
                time.sleep(5)
            print("Ready to Trade Now and Spread < 2")
            print(ticker)
        else: 
            ticker = c.get_ticker(pair=trade_pair)
            last_bid = float(ticker["bid"])
            last_ask = float(ticker["ask"])
            last_trade = float(ticker["last_trade"])
            spread_act = last_ask - last_bid
            print("volatile Spread at moment is ",spread_act)
                 
        ####how much BTC volume & and what price willing to buy######
        my_bid_rate = last_bid + 1 ##########to ensure sellers take my bid first, and the first trigger
        stop_bid_rate = my_bid_rate + 10 ######maximum i could pay more than the market
        btc_to_buy = round(((1/my_bid_rate) * minpurchase),precission) #max can have 6 decimal only
        
        ################Only to be used when mininum amount need to uchase. otherwise comment and topup rquired money
        btc_to_buy = min_btc_to_buy  ###remove when not in use for testing
        
        #To Make sure the balance money you have enough to use for trading
        account_sid = 'XXX' 
        auth_token = 'XXX' 
        client = twilio(account_sid, auth_token) 
        if mybal <= (last_bid*btc_to_buy): 
            message = client.messages.create( 
                              from_='whatsapp:+141XXX',  
                              body='Your crypto order of 0.0005 has failed becuase not enough balance on 2019. Details: topup crypto else will eat other savings money',      
                              to='whatsapp:+60XXX' 
                          ) 
            print(message.sid);
            
            #####write status of last buy
            f = open("xxx\\buy_status.txt", "a")
            f.write(str(today))
            f.write("Your crypto order of 0.0005 has failed becuase not enough balance today.topup crypto else will eat other additional savings")
            f.close()
            
          
        else:
            #####write status of last buy
            f = open("xxx\\buy_status.txt", "a")
            f.write(str(today))
            f.write("Your crypto order of 0.0005 was successful")
            f.close()
        
            n=1;
        
        
        #####write the purchase price
        f = open("XXX\\last_purchase_price.txt", "w")
        f.write(str(stop_bid_rate))
        f.close()
        
        #####write last purchase volume volume
        f = open("XXX\\last_purchase_volume.txt", "w")
        f.write(str(btc_to_buy))
        f.close()
        
 
  ##############limit_order_not working#########################################  

        limit_order = c.post_limit_order(trade_pair, type = 'BID', volume = btc_to_buy, price = stop_bid_rate, stop_price = my_bid_rate, stop_direction = 'ABOVE', base_account_id=None, counter_account_id = bid_accnt_id)
 
  ###############################################################################
        max_no_order -= 1




except Exception as e:
  print(e)


  
  
  
  
