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
import random
import time


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.httpRequests import httpClientBuild


class DoCrawlingJob(MessagingHandler):
    def __init__(self, server, httpClient):
        super(DoCrawlingJob, self).__init__()
        self.server = server
        self.httpClient = httpClient
        self.consumerId = "basic_worker_2"
        self.mission = "DoCrawlingJob"

    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        , "amq.topic/the_producer.crawling_list"
                                                        , options=Selector("LaborNo = '2'"))
        self.sender = event.container.create_sender(conn, "amq.direct/workers_reply")
        
        

    def on_message(self, event):
        """
        msgJson
        [('8151/151/016.jpg', 'Consumers_2/電鋸人/第151話/016.jpg')] 
        """
        time.sleep(2)
        print(f"<<<<<<< {self.consumerId} on_message begins : {self.mission}")
        msgJson = json.loads(event.message.body)
        
        print(f"Received property of msg：\n{json.dumps(event.message.properties, indent=2, ensure_ascii=False)}")

        
        if event.message.properties["TotalUrlNum"] == "0":

            pass
        else:
            # handling

            for row in msgJson:
                self.httpClient.downloadPage(row[0], row[1])
                time.sleep(0.5 + random.random() * 0.5)


        self.sender.send(Message(body="done"
                                , id = self.consumerId))            
            
        self.sender.close()
        event.connection.close()
        print(f">>>>>>> {self.consumerId} on_message done")




if __name__ ==  '__main__':

    try:
        httpClient = httpClientBuild()
        Container(DoCrawlingJob("localhost:5672", httpClient)).run()
    except KeyboardInterrupt as e:
        
 
        
        pass
    