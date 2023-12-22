from proton import Message,symbol, ulong, PropertyDict, Described
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector, Filter, Copy, ReceiverOption
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

    """
    rxheaders = ssn.receiver("match-q;
                            {create: always
                            , node: {type: queue}
                            , link:{x-bindings:[{key: 'binding-name'
                                            , exchange: 'amq.match'
                                            , queue: 'match-q'
                                            , arguments:{'x-match': 'any', 'header1': 'value1'}
                                            }]
                                    }
                            }")

    connection.open_receiver({source:{address:'amq.match', filter:{'foo':amqp_types.wrap_described({'nat': 'it','prod': 'a22', 'x-match': 'all'}, 0x468C00000002)}}});                                            
    """

    def on_start(self, event):
        
        b = Described(symbol('two'), "match-p;{create: always, node: {type: queue}, link:{x-bindings:[{key: 'binding-name', exchange: 'amq.match', queue: 'match-p', arguments:{'x-match': 'any', '1': 'apple'}}]}}")
        a = {symbol('two'):b}
        conn = event.container.connect(self.server, password="guest", user ="guest" )

        
        self.receiver = event.container.create_receiver(conn
                                                        , "amq.topic/the_producer.hot_comic_today"
                                                        , options=Selector("colour = 'gree'"))
                                                        
        
        
        self.sender = event.container.create_sender(conn, "amq.direct/consumers_reply")
        

    def on_message(self, event):

        
        print(f"received comics today：\n{json.dumps(json.loads(event.message.body), indent=2)}")

        chosenNum = input('choose which comics you want: \n')
        
        self.sender.send(Message(body=f"{chosenNum}"))
        print(f"sent back to producer：{chosenNum} ")
        self.sender.close()
        # event.connection.close()




if __name__ ==  '__main__':

    try:
        
        Container(HelloWorld("localhost:5672")).run()
    except KeyboardInterrupt as e:
        
 
        
        pass
    