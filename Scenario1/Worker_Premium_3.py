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


chosenNum = 999

class HelloWorld(MessagingHandler):
    def __init__(self, server):
        super(HelloWorld, self).__init__()
        self.server = server


    def on_start(self, event):
        
        # b = Described(symbol('two'), "match-p;{create: always, node: {type: queue}, link:{x-bindings:[{key: 'binding-name', exchange: 'amq.match', queue: 'match-p', arguments:{'x-match': 'any', '1': 'apple'}}]}}")
        # a = {symbol('two'):b}
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        , "amq.topic/the_producer.crawling_list"
                                                        , options=Selector("LaborNo = '3'"))
        self.sender = event.container.create_sender(conn, "amq.direct/workers_reply")
        
        

    def on_message(self, event):

        
        print(f"received works：\n{json.dumps(json.loads(event.message.body), indent=2)}")

        #chosenNum = input('choose which comics you want: \n')
        print(json.dumps(event.message.properties))
        self.sender.send(Message(body=f"{chosenNum}"))
        print(f"sent back to producer from worker：{chosenNum} ")
        self.sender.close()
        event.connection.close()




if __name__ ==  '__main__':

    try:
        
        Container(HelloWorld("localhost:5672")).run()
    except KeyboardInterrupt as e:
        
 
        
        pass
    