from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time


class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        event.container.create_sender(conn, "amq.topic/*")
        event.container.create_receiver(conn, "amq.topic/*.*")

    def on_message(self, event):
        print(f"received：{event.message.body}")
        

    def on_sendable(self, event):
        
        for i in range(5):
            event.sender.send(Message(body=f"Hello World!_{i}"))
            print(f"sent：Hello World!_{i}")
            event.sender.close()
            time.sleep(1)            
            # break
          
        # event.connection.close()        
        

try:
    Container(HelloWorld("localhost:5672", "amq.topic/1")).run()
except KeyboardInterrupt as e:
    pass