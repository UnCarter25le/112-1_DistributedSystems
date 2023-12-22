import sys
from qpid.messaging import *
import time

broker =  "localhost:5672" if len(sys.argv)<2 else sys.argv[1]
address = "amq.topic" if len(sys.argv)<3 else sys.argv[2]

#connection = Connection(broker)

connection = Connection(broker,
                  username ="guest",
                  password="guest")
#, user="guest", password="guest"

try:
    connection.open()  #(1)
    
    session = connection.session()   #(2)

    sender = session.sender(address)  #(3)
    #receiver = session.receiver(address)  #(4)
    rxheaders = session.receiver("match-q;{create: always, node: {type: queue}, link:{x-bindings:[{key: 'binding-name', exchange: 'amq.match', queue: 'match-q', arguments:{'x-match': 'any', '1': 'apple'}}]}}")
    time.sleep(5)
    sender.send(Message("Hello world!"));

    message = rxheaders.fetch(timeout=1)  #(5)
    print (message.content)
    session.acknowledge() #(6)

except MessagingError as m:
    print (m)
finally:
    connection.close()  #(7)