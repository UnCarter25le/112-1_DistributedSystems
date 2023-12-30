# -*- coding:utf-8 -*-
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, AtMostOnce
import time
import json
import os
import sys



_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.httpRequests import httpClientBuild
from libs.manipulateDir import folderDataManipulate


"""
{
  "1": {
    "comic": "DRAWING 最強漫畫家利用繪畫技能在異世界開無雙！",
    "comicUrl": "https://tw.manhuagui.com/comic/42802/"
  },
  "2": {
    "comic": "27歲的OL、在異世界開始管理遊女",
    "comicUrl": "https://tw.manhuagui.com/comic/47442/"
  },
}
"""
class DeliverHotComicToday(MessagingHandler):
    global hotComicTodayJson
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
        msgForSend = {}
        for ordinal, kvobj in hotComicTodayJson.items():
            comic = kvobj["comic"] 
            status = kvobj["comicStatus"] 
            msgForSend[ordinal] = {"comic" : comic, "status" : status}
        self.sender.send(Message(body=json.dumps(msgForSend, ensure_ascii=False)
                                , properties={'TheProducerSent': "yes", 'HotComicToday': "yes" }
                                ,  id = "TheProducer"))
        
        self.sender.close()
        event.connection.close()   
        print(f">>>>>>> TheProducer on_sendable done")         
        

class ReceiveComicListChosen(MessagingHandler):
    global hotComicTodayJson
    def __init__(self, server, httpClient, folderManipulator):
        super(ReceiveComicListChosen, self).__init__()
        self.server = server
        self.httpClient = httpClient
        self.folderManipulator = folderManipulator
        self.feedbacknum = 0
        self.forsureDoingNum = 0
        self.mission = "ReceiveComicListChosen"
        self.comicChosenDict = {}
        


    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender =  event.container.create_sender(conn, "amq.topic/the_producer.crawling_list")
        self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply")
        

    def on_message(self, event):
        """
        msgJson
        {
            "comic": {
                "ordinal": "2",
                "name": "DragonBall Z"
            }
        }            
        """
        
        whichConsumer = event.message.id
 
        if whichConsumer in ["Consumers_1", "Consumers_2"]:
            self.feedbacknum += 1
            if self.feedbacknum == 1:
                print(f"<<<<<<< TheProducer on_message, on_sendable begins : {self.mission}")   
            msgJson = json.loads(event.message.body)
            msgJsonStr = json.dumps(msgJson, indent=2, ensure_ascii=False)                   
            print(f"Received msg from {whichConsumer}")
            print(f"{whichConsumer} choose：{msgJsonStr}")
            
            comicName = msgJson["comic"]["name"]["comic"]
            ordinal = msgJson["comic"]["ordinal"]
            if comicName == "q":
                pass
            else:
                self.forsureDoingNum += 1
                """
                self.comicChosenDict
                {   
                    'ONE PIECE航海王': {'ordinal': '1', 'consumers': ['Consumers_1']}
                    , '27歲的OL、在異世界開始管理遊女': {'ordinal': '2', 'consumers': ['Consumers_2']}
                }

                """
                if len(self.comicChosenDict) == 0:
                    self.comicChosenDict= {comicName : { "ordinal" : ordinal, "consumers" : [whichConsumer]}}
                else:
                    if comicName not in self.comicChosenDict:
                        self.comicChosenDict[comicName] =  { "ordinal" : ordinal, "consumers" : []}
                    self.comicChosenDict[comicName]["consumers"].append(whichConsumer)
            
            if self.feedbacknum == 2:
                if self.forsureDoingNum >= 1 and len(self.comicChosenDict) != 0:
                    print("Preparing urls for sending to workers:")
                    # check if folder exists
                    tmp = self.comicChosenDict
                    for comic, kvobj in tmp.items():
                        latestEpisode = hotComicTodayJson[kvobj["ordinal"]]["comicStatus"]
                        comicUrl = hotComicTodayJson[kvobj["ordinal"]]["comicUrl"]
                        for consumer in kvobj["consumers"]:
                            folderManipulator.mkdirForRawData(f"HotComicToday/{consumer}/{comic}/{latestEpisode}")

                        self.comicChosenDict[comic]["comicUrl"] = comicUrl
                    # crawling urls list
                    totalUrlDict = []
                    for comic, kvobj in self.comicChosenDict.items():
                        comicUrl = self.comicChosenDict[comic]["comicUrl"]
                        
                        comicNumCode = comicUrl.split("/")[-1].replace(".html", "")

                        episodeJson = httpClient.getEpisode(comicUrl)
                        limitPage = int(episodeJson["limitPage"])
                        latestEpisode = episodeJson["episode"]
                        latestEpisodeNum = latestEpisode.replace("第", "").replace("話", "")
                        
                        for i in range(limitPage):
                            i += 1
                            pageNum = f"00{i}" if len(str(i)) == 1 else f"0{i}"
                            tmpUrl = f"{comicNumCode}/{latestEpisodeNum}/{pageNum}.jpg"
                            for consumer in kvobj["consumers"]:
                                filepath = f"{consumer}/{comic}/{latestEpisode}/{pageNum}.jpg"
                                totalUrlDict.append((tmpUrl, filepath))

                    """
                    [('8151/151/016.jpg', 'Consumers_2/電鋸人/第151話/016.jpg')] 
                    """



                    # calculate and distribute
                    totalNumForSend = len(totalUrlDict)
                    workerNum = 2 if totalNumForSend <= 20 else 3
                    dividedBenchNum = (totalNumForSend // workerNum) + (1 if totalNumForSend % workerNum > 0 else 0)
                    
                    print(f"totalNumForSend : {totalNumForSend}", f"workerNum : {workerNum}", f"dividedBenchNum : {dividedBenchNum}")

                    if workerNum == 2:
                    
                        
                        self.sender.send(Message(body=json.dumps(totalUrlDict[0:dividedBenchNum], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : f"{dividedBenchNum}", 'LaborNo': '1'} # 'premium-labor': 'yes' # "consumers" : json.dumps(self.comicChosenDict[comicName]["consumers"])
                                                
                                                ))        
                        #
                        self.sender.send(Message(body=json.dumps(totalUrlDict[dividedBenchNum:], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : f"{totalNumForSend-dividedBenchNum+1}", 'LaborNo': '2'} 
                                                
                                                ))    
                        self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : '0', 'LaborNo': '3'} 
                                                
                                                ))                            
                    else:
                        # scalability depends on needs  
                        self.sender.send(Message(body=json.dumps(totalUrlDict[0:dividedBenchNum], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : f"{dividedBenchNum}", 'LaborNo': '1'} # 'premium-labor': 'yes' # "consumers" : json.dumps(self.comicChosenDict[comicName]["consumers"])
                                                
                                                ))        
                        
                        self.sender.send(Message(body=json.dumps(totalUrlDict[dividedBenchNum:dividedBenchNum*2], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : f"{dividedBenchNum}", 'LaborNo': '2'} 
                                                
                                                ))                            
                        self.sender.send(Message(body=json.dumps(totalUrlDict[dividedBenchNum*2:], ensure_ascii=False)
                                                
                                                , properties={'TotalUrlNum' : f"{totalNumForSend-dividedBenchNum*2+1}", 'LaborNo': '3'} 
                                                
                                                ))                       
                            

                    

                    print("done")



                else:
                    print("Notify workers to sleep:")
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '1'} 
                                            
                                            ))        
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '2'} 
                                            
                                            ))  
                    self.sender.send(Message(body=json.dumps([], ensure_ascii=False)
                                            
                                            , properties={'TotalUrlNum' : '0', 'LaborNo': '3'} 
                                            
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
    global comicInfoShared
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
    httpClient = httpClientBuild()
    hotComicTodayJson = httpClient.getHotComicList()
    folderManipulator = folderDataManipulate()
    hotComicToday = Container(DeliverHotComicToday("localhost:5672"))
    hotComicToday.container_id = "TheProducer"    
    comicListChosen = Container(ReceiveComicListChosen("localhost:5672", httpClient, folderManipulator))
    comicListChosen.container_id = "TheProducer"
    workerCondition = Container(ReceiveWorkerCondition("localhost:5672"))
    workerCondition.container_id = "TheProducer"
    
    hotComicToday.run()
    comicListChosen.run()
    workerCondition.run()
except KeyboardInterrupt as e:
    pass