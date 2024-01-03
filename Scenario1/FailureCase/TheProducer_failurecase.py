# -*- coding:utf-8 -*-
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, AtMostOnce
import time
import json

chosenNum = 999

class HelloWorld(MessagingHandler):
    
    def __init__(self, server):
        super(HelloWorld, self).__init__()
        self.server = server
        self.producer1 = 0
        self.producer2 = 0
        self.producer3 = 0
        self.conn = 0
        
    
    def on_start(self, event):
        
        self.conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.producer1 = event.container.create_sender(self.conn
                                                    , "amq.topic/the_producer.hot_comic_today", options=AtMostOnce())
                                                    #, "amq.match")
        
        self.receiver = event.container.create_receiver(self.conn, "amq.direct/consumers_reply", options=AtMostOnce())
        
        
        
        self.producer2 = event.container.create_sender(self.conn, "amq.topic/the_producer.crawling_list")
        
        
        # self.receiver2 = event.container.create_receiver(conn, "amq.direct/workers_reply")
        

    def on_message(self, event):

        print(f"consumer choose：{event.message.body}")

        print("send to worker")

        # time.sleep(2)
        self.producer1.send(Message(body=json.dumps({"4" : "apple", "24" : "bananan"})
                                , properties={'colour': "gree", 'colour1': "gree1" }
                                
                                #, properties={'basic-labor': 'yes', 'premium-labor': 'yes'}
                                ,  id = "aaaaaaaaaaaaa"))
        
        self.producer1.close()
        
        for n in range(2):
            self.producer2.send(Message(body=json.dumps({"1" : "apple", "2444444" : "bananan"})
                                    #, properties={'colour': "gree", 'colour1': "gree1" }
                                    
                                    #, properties={'basic-labor' : 'yes', 'premium-labor' : 'yes'}
                                    ))        
        
        self.producer2.close()  
             

        print(111)
        event.connection.close()        

       

    def on_sendable(self, event):        
            
        
        self.producer1.send(Message(body=json.dumps({"1" : "apple", "2" : "bananan"})
                                , properties={'colour': "gree", 'colour1': "gree1" }
                                
                                #, properties={'basic-labor': 'yes', 'premium-labor': 'yes'}
                                ,  id = "aaaaaaaaaaaaa"))
        
        
        self.producer1.close()
        


        # event.connection.close()        
        

try:
    Container(HelloWorld("localhost:5672")).run()
except KeyboardInterrupt as e:
    pass