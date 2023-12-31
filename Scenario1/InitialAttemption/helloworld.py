from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time



server = "localhost:5672"
address = "amq.topic"


ctainer = Container()
ctainer.run()

conn = ctainer.connect(server, password="guest", user ="guest" )


sender = ctainer.create_sender(conn, address)
receiver = ctainer.create_receiver(conn, address)

# print(2)
sender.send(Message(body="Hello World!"))
#sender.close()
#print(3)
#time.sleep(1)

conn.close()

