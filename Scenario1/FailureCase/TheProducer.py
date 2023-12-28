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
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender = event.container.create_sender(conn
                                                    , "amq.topic/the_producer.hot_comic_today", options=AtMostOnce())
                                                    #, "amq.match")
        
        # self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply", options=AtMostOnce())
        
        
        # self.receiver2 = event.container.create_receiver(conn, "amq.direct/workers_reply")
        

    def on_message(self, event):

        print(f"consumer choose：{event.message.body}")

        print("send to worker")

        
        
        # for n in range(2):
        #     self.producer2.send(Message(body=json.dumps({"1" : "apple", "2444444" : "bananan"})
        #                             #, properties={'colour': "gree", 'colour1': "gree1" }
                                    
        #                             #, properties={'basic-labor' : 'yes', 'premium-labor' : 'yes'}
        #                             ))        
        
        # self.producer2.close()  
             

        print(111)
        event.connection.close()        

       

    def on_sendable(self, event):        
            
        
        self.sender.send(Message(body=json.dumps({"1" : "apple", "2" : "bananan"})
                                , properties={'colour': "gree", 'colour1': "gree1" }
                                
                                #, properties={'basic-labor': 'yes', 'premium-labor': 'yes'}
                                ,  id = "aaaaaaaaaaaaa"))
        
        
        self.sender.close()
        


        event.connection.close()        
        

class HelloWorld2(MessagingHandler):
    
    def __init__(self, server):
        super(HelloWorld2, self).__init__()
        self.server = server
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn, "amq.topic/the_producer.crawling_list")
        
        self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply", options=AtMostOnce())
        
        
        
        

    def on_message(self, event):

        print(f"consumer choose：{event.message.body}")

        print("send to worker")

        
        
        # for n in range(2):
        self.sender.send(Message(body=json.dumps({"1" : "apple", "2444444" : "bananan"})
                                #, properties={'colour': "gree", 'colour1': "gree1" }
                                
                                #, properties={'basic-labor' : 'yes', 'premium-labor' : 'yes'}
                                ))        
        
        self.sender.close()  
             

        print(111)
        event.connection.close()        

       

    def on_sendable(self, event):        
            
        pass
        # self.sender.send(Message(body=json.dumps({"1" : "apple", "2" : "bananan"})
        #                         , properties={'colour': "gree", 'colour1': "gree1" }
                                
        #                         #, properties={'basic-labor': 'yes', 'premium-labor': 'yes'}
        #                         ,  id = "aaaaaaaaaaaaa"))
        
        
        # self.sender.close()
        


        # event.connection.close()        
                

try:
    a = Container(HelloWorld("localhost:5672"))
    b = Container(HelloWorld2("localhost:5672"))
    a.run()
    b.run()
except KeyboardInterrupt as e:
    pass