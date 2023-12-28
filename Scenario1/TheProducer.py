# -*- coding:utf-8 -*-
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, AtMostOnce
import time
import json

chosenNum = 999

class DeliverHotComicToday(MessagingHandler):
    
    def __init__(self, server):
        super(DeliverHotComicToday, self).__init__()
        self.server = server
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender = event.container.create_sender(conn
                                                    , "amq.topic/the_producer.hot_comic_today")
                                                    #, "amq.match")

    def on_message(self, event):
        pass   

       
    def on_sendable(self, event):        
        self.sender.send(Message(body=json.dumps({"1" : "20th Century Boys", "2" : "DragonBall Z", "3" :"Crayon Shin-chan"})
                                , properties={'TheProducerSent': "yes", 'HotComicToday': "yes" }
                                ,  id = "FromTheProducer"))
        self.sender.close()
        event.connection.close()        
        

class ReceiveComicListChosen(MessagingHandler):
    
    def __init__(self, server):
        super(ReceiveComicListChosen, self).__init__()
        self.server = server
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn, "amq.topic/the_producer.crawling_list")
        self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply")
        
    def on_message(self, event):

        print(f"consumer choose：{event.message.body}")
        print("send to worker")

        self.sender.send(Message(body=json.dumps(['http://localhost.com', 'http://localhost.com'])
                                
                                , properties={'TotalUrlNum' : '50', 'LaborNo': '1'} # 'premium-labor': 'yes'
                                
                                ))        
        self.sender.send(Message(body=json.dumps(['http://localhost.com', 'http://localhost.com', 'http://localhost.com'])
                                
                                , properties={'TotalUrlNum' : '50', 'LaborNo': '2'} # 'premium-labor': 'yes'
                                
                                ))          
        self.sender.close()  
        event.connection.close()        

       

    def on_sendable(self, event):        
            
        pass


class ReceiveWorkerCondition(MessagingHandler):
    
    def __init__(self, server):
        super(ReceiveWorkerCondition, self).__init__()
        self.server = server
        self.feedbacknum = 0
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn, "amq.topic/the_producer.hot_comic_today")
        
        self.receiver = event.container.create_receiver(conn, "amq.direct/workers_reply")
        
    def on_message(self, event):
        self.feedbacknum += 1
        print(f"worker feedback：{event.message.body}")
        
        if self.feedbacknum >= 2:
            event.connection.close()      

        
        self.sender.send(Message(body="Mission Complete!"
                                , properties={'TheProducerSent': "yes", 'HotComicToday': "done" }
                                ,  id = "FromTheProducer"))
   
        self.sender.close()  
        event.connection.close()        

       

    def on_sendable(self, event):        
            
        pass


try:
    hotComicToday = Container(DeliverHotComicToday("localhost:5672"))
    comicListChosen = Container(ReceiveComicListChosen("localhost:5672"))
    workerCondition = Container(ReceiveWorkerCondition("localhost:5672"))
    
    hotComicToday.run()
    comicListChosen.run()
    workerCondition.run()
except KeyboardInterrupt as e:
    pass