from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container, Selector
import time
import json


class HelloWorld(MessagingHandler):
    def __init__(self, server):
        super(HelloWorld, self).__init__()
        self.server = server

    def on_start(self, event):
        
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        self.sender = event.container.create_sender(conn
                                                    #, "amq.topic/the_producer.hot_comic_today")
                                                    , "amq.match")
                                                    
        self.receiver = event.container.create_receiver(conn, "amq.direct/consumers_reply")
        

    def on_message(self, event):

        print(f"consumer choose：{event.message.body}")
        

    def on_sendable(self, event):

        time.sleep(1)
        event.sender.send(Message(body=json.dumps({"1" : "apple", "2" : "bananan"})
                                  #, properties={'colour': "gree"}
                                  , properties={"x-match":"any", "1" : "apple"}
                                  ,  id = "aaaaaaaaaaaaa"))
        event.sender.close()
        
        # event.connection.close()        
        

try:
    Container(HelloWorld("localhost:5672")).run()
except KeyboardInterrupt as e:
    pass