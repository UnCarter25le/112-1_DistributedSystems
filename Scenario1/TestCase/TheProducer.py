# -*- coding:utf-8 -*-
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, AtMostOnce
import time
import json
import os
import sys



_BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import folderDataManipulate

class DeliverHotComicToday(MessagingHandler):
    
    def __init__(self, server):
        super(DeliverHotComicToday, self).__init__()
        self.server = server
        self.mission = "DeliverHotComicToday"
    
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender = event.container.create_sender(conn
                                                    , "amq.topic/the_producer.hot_comic_today")
                                                    #, "amq.match")

       
    def on_sendable(self, event):    
        print(f"<<<<<<< TheProducer on_sendable begins : {self.mission}")    

        self.sender.send(Message(body=json.dumps({"1" : "20th Century Boys", "2" : "DragonBall Z", "3" :"Crayon Shin-chan"})
                                , properties={'TheProducerSent': "yes", 'HotComicToday': "yes" }
                                ,  id = "FromTheProducer"))
        self.sender.close()
        event.connection.close()   
        print(f">>>>>>> TheProducer on_sendable done")         
        

class ReceiveComicListChosen(MessagingHandler):
    
    def __init__(self, server, folderManipulator):
        super(ReceiveComicListChosen, self).__init__()
        self.server = server
        self.folderManipulator = folderManipulator
        self.feedbacknum = 0
        self.forsureDoingNum = 0
        self.mission = "ReceiveComicListChosen"
        self.comicNameList = []


    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn, "amq.topic/the_producer.crawling_list")
        self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply")
        
    def on_message(self, event):

         
        whichConsumer = event.message.id
 
        if whichConsumer in ["Consumers_1", "Consumers_2"]:
            self.feedbacknum += 1
            if self.feedbacknum == 1:
                print(f"<<<<<<< TheProducer on_message, on_sendable begins : {self.mission}")   
            msgJson = json.loads(event.message.body)
            msgJsonStr = json.dumps(msgJson, indent=2, ensure_ascii=False)                   
            print(f"Received msg from {whichConsumer}")
            print(f"{whichConsumer} choose：{msgJsonStr}")

            if msgJson["comic"]["name"] == "q":
                pass
            else:
                self.forsureDoingNum += 1
                self.comicNameList.append(msgJson["comic"]["name"])

            if self.feedbacknum == 2 and len(self.comicNameList) == 2:
                if self.forsureDoingNum >= 1:
                    # de duplicated comic name
                    comicNameSet = set(self.comicNameList)
                    print(comicNameSet)
                    print("Preparing urls for sending to workers:")

                    # check folder
                    for row in comicNameSet:
                        folderManipulator.mkdirForRawData(f"HotComicToday/{row}")

                    # crawling urls list


                    # calculate and distribute

                    

                    self.sender.send(Message(body=json.dumps(['http://localhost.com', 'http://localhost.com'], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '50', 'LaborNo': '1', "Comic" : msgJson["comic"]["name"]} # 'premium-labor': 'yes'
                                            
                                            ))        
                    self.sender.send(Message(body=json.dumps(['http://localhost.com', 'http://localhost.com', 'http://localhost.com'], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '50', 'LaborNo': '2', "Comic" : msgJson["comic"]["name"]} # 'premium-labor': 'yes'
                                            
                                            ))    
                    # scalability depends on needs  
                    self.sender.send(Message(body=json.dumps(['http://localhost.com', 'http://localhost.com', 'http://localhost.com'], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '50', 'LaborNo': '3', "Comic" : msgJson["comic"]["name"]} 
                                            
                                            ))                       
                          

                    

                    print("done")



                else:
                    print("Notify workers to sleep:")
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '1', "Comic" : msgJson["comic"]["name"]} 
                                            
                                            ))        
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '2', "Comic" : msgJson["comic"]["name"]} 
                                            
                                            ))  
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '3', "Comic" : msgJson["comic"]["name"]} 
                                            
                                            ))                               
                    
                    print("done")
                self.sender.close()  
                event.connection.close()
                print(f">>>>>>> TheProducer on_message, on_sendable done")    
        else:
            pass

    def on_sendable(self, event):        
            
        pass


class ReceiveWorkerCondition(MessagingHandler):
    
    def __init__(self, server):
        super(ReceiveWorkerCondition, self).__init__()
        self.server = server
        self.feedbacknum = 0
        self.mission = "ReceiveWorkerCondition"

    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn
                                                     #, "amq.topic/the_producer.hot_comic_today")
                                                     , "amq.fanout")
        
        self.receiver = event.container.create_receiver(conn, "amq.direct/workers_reply")
        
    def on_message(self, event):
        self.feedbacknum += 1
        if self.feedbacknum  == 1:
            print(f"<<<<<<< TheProducer on_message, on_sendable begins : {self.mission}")    
        print(f"Received {event.message.id} feedback：{event.message.body}")
        

       
 
        if self.feedbacknum == 3:

            self.sender.send(Message(body="Mission Complete!"
                                    , properties={'TheProducerSent': "yes", 'HotComicToday': "done" }
                                    ,  id = "TheProducer"))
    
            print(f">>>>>>> TheProducer on_message, on_sendable done")
            self.sender.close()  
            event.connection.close()    
    

       

    def on_sendable(self, event):        
            
        pass


try:
    
    folderManipulator = folderDataManipulate()
    hotComicToday = Container(DeliverHotComicToday("localhost:5672"))
    hotComicToday.container_id = "TheProducer"
    comicListChosen = Container(ReceiveComicListChosen("localhost:5672", folderManipulator))
    comicListChosen.container_id = "TheProducer"
    workerCondition = Container(ReceiveWorkerCondition("localhost:5672"))
    workerCondition.container_id = "TheProducer"
    
    hotComicToday.run()
    comicListChosen.run()
    workerCondition.run()
except KeyboardInterrupt as e:
    pass