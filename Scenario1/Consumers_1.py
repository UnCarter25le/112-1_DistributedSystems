# -*- coding:utf-8 -*-
from proton import Message,symbol, ulong, PropertyDict, Described
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, Filter, Copy, ReceiverOption, AtMostOnce
import time
import multiprocessing as mp
from threading import Thread
import threading
import sys
import json
import os

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

class WaitForComicList(MessagingHandler):
    def __init__(self, server):
        super(WaitForComicList, self).__init__()
        self.server = server
        self.chosenNum = 0
        self.producerMode = {"1" : "basic", "2" : "basic+premium"}
        self.consumerId = "Consumers_1"
        self.mission = "WaitForComicList"


    def on_start(self, event):
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        , "amq.topic/the_producer.hot_comic_today" 
                                                        , options=Selector("TheProducerSent = 'yes' AND HotComicToday = 'yes'"))
                                                        
        
        self.sender = event.container.create_sender(conn, "amq.direct/consumers_reply")
        

    def on_message(self, event):
        """
        msgJson
        {
        "1": "20th Century Boys",
        "2": "DragonBall Z",
        "3": "Crayon Shin-chan"
        }
        {
            "8": {
                "comic": "DR.STONE",
                "status": "第232話"
            },
            "9": {
                "comic": "進擊的巨人",
                "status": "第139話"
            }
        }   
        """
        print(f"<<<<<<< {self.consumerId} on_message begins: {self.mission}")
        msgJson = json.loads(event.message.body)
        msgJsonStr = json.dumps(json.loads(event.message.body), indent=2 , ensure_ascii=False)
        modeJsonStr = json.dumps(self.producerMode, indent=2 , ensure_ascii=False)
        print(f"Received comics today：\n{msgJsonStr} \n ; if no need, enter q")
        # print(f"There are two producer mode for choosing：\n{modeJsonStr}")
        chosenNum = input('【choose which comics you want:】 \n')

        while True:
            if chosenNum == "q":
                break
            elif chosenNum == "":
                chosenNum = 0       
            tmp = int(chosenNum)
            if(0 < tmp <= len(msgJson)):
                break
            else:
                chosenNum = input('number should be on the list;choose which comics you want: \n')


        if chosenNum != "q":
            # chosenMode = input('【2】choose which producer mode you want: \n')
            # while True:
            #     tmp = int(chosenMode)
            #     if(tmp in [1 ,2]):
            #         break
            #     else:
            #         chosenMode = input('number should be on the list;choose which producer mode you want: \n')

            msgBack = {"comic": {"ordinal" : chosenNum , "name" : msgJson[chosenNum]}} 
            # msgBack = {"comic": {"ordinal" : chosenNum , "name" : msgJson[chosenNum]},
            #         "mode" : { "ordinal" : chosenMode , "name" : self.producerMode[chosenMode]}}
                       
        else:
            msgBack = {"comic": {"ordinal" : "" , "name" : {"comic":"q", "status":"q"}}}     
            # msgBack = {"comic": {"ordinal" : "" , "name" : "q"},
            #         "mode" : { "ordinal" : "" , "name" : "q"}}     
        self.sender.send(Message(body=json.dumps(msgBack, ensure_ascii=False)
                                ,  id = self.consumerId))
        print(f">>>>>>>{self.consumerId} on_message done")
        self.sender.close()
        event.connection.close()


class WaitForComplete(MessagingHandler):
    def __init__(self, server):
        super(WaitForComplete, self).__init__()
        self.server = server
        self.consumerId = "Consumers_1"
        self.mission = "WaitForComplete"
    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        #, "amq.topic/the_producer.hot_comic_today" 
                                                        , "amq.fanout" 
                                                        , options=Selector("TheProducerSent = 'yes' AND HotComicToday = 'done'"))
                                                        
    def on_message(self, event):

        print(f"<<<<<<< {self.consumerId} on_message begins : {self.mission}")
        print(f"Received comics complete：\n{event.message.body}")
        event.connection.close()
        print(f">>>>>>>{self.consumerId} on_message done")


if __name__ ==  '__main__':

    try:
        
        waitForComicList = Container(WaitForComicList("localhost:5672"))
        waitForComplete = Container(WaitForComplete("localhost:5672"))
        waitForComicList.run()
        waitForComplete.run()
    except KeyboardInterrupt as e:
        pass
    