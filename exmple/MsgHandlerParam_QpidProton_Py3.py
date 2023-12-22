from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__() # here :super(HelloWorld, self).__init__(prefetch=10)
        self.server = server
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        event.container.create_receiver(conn, "amq.topic/*.*.*") #binding key
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        event.sender.send(Message(body="Hello World!"))#, id = "aa", subject="aa"))#, properties={'colour': 'red'})) #<--- application properties
        event.sender.close()

    def on_message(self, event):
        print(event.message.body)
        event.connection.close()


Container(HelloWorld("localhost:5672", "amq.topic/1.2.3")).run() # routing key