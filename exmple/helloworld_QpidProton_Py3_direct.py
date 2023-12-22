from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        event.container.create_receiver(conn, self.address)
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        event.sender.send(Message(body="Hello World!"))
        event.sender.close()

    def on_message(self, event):
        print(event.message.body)
        event.connection.close()


Container(HelloWorld("localhost:5672", "amq.topic")).run()
# guest:guest@localhost:5672 可以替代connect帶入帳密
# real url : amqp://guest:guest@localhost:5672
#DEPRECATED https://qpid.apache.org/releases/qpid-proton-0.33.0/proton/python/docs/proton.html#proton.Url