from twilio.rest import Client 
 
        ###sends sms to your own watasapp no whether you are holding or not.
        account_sid = 'xxx' 
        auth_token = 'xx' 
        client = Client(account_sid, auth_token) 
        if growth <= 2.5:         
            message = client.messages.create( 
                              from_='whatsapp:+141xxx',  
                              body='For this week crypto growth is less than 2.5% cannot trade now, hodling or you decide to stop trade ',      
                              to='whatsapp:+60xxx' 
                          ) 
            print(message.sid);
        else:
            message = client.messages.create( 
                              from_='whatsapp:+141xxx',  
                              body='For this week crypto growth is less than 2.5% cannot trade now, hodling or you decide to stop trade ',      
                              to='whatsapp:+60xxx' 
                          ) 
            print(message.sid);

            a =1