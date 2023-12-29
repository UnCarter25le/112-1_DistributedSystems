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

class DoCrawlingJob(MessagingHandler):
    def __init__(self, server):
        super(DoCrawlingJob, self).__init__()
        self.server = server
        self.consumerId = "premium_worker_3"
        self.mission = "DoCrawlingJob"

    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        , "amq.topic/the_producer.crawling_list"
                                                        , options=Selector("LaborNo = '3'"))
        self.sender = event.container.create_sender(conn, "amq.direct/workers_reply")
        
        

    def on_message(self, event):
        time.sleep(2)
        print(f"<<<<<<< {self.consumerId} on_message begins : {self.mission}")
        msgJson = json.loads(event.message.body)
        
        print(f"Received property of msg：\n{json.dumps(event.message.properties, indent=2, ensure_ascii=False)}")

        
        if event.message.properties["Comic"] == "q":


            self.sender.send(Message(body="done"
                                    , id = self.consumerId))
        else:
            # handling
            self.sender.send(Message(body="done"
                                    , id = self.consumerId))            
            
        self.sender.close()
        event.connection.close()
        print(f">>>>>>> {self.consumerId} on_message done")




if __name__ ==  '__main__':

    try:
        
        Container(DoCrawlingJob("localhost:5672")).run()
    except KeyboardInterrupt as e:
        
 
        
        pass
    