# -*- coding:utf-8 -*-
import sys
from qpid.messaging import *
import time
import json

broker =  "localhost:5672" if len(sys.argv)<2 else sys.argv[1]
address = "amq.match" if len(sys.argv)<3 else sys.argv[2]

#connection = Connection(broker)
connection = Connection(broker,
                  username ="guest",
                  password="guest")
#, user="guest", password="guest"


try:

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
    """

    connection.open()  #(1)
    
    session = connection.session()   #(2)

    sender = session.sender(address)  #(3)
    #receiver = session.receiver(address)  #(4) error:Bindings to an exchange of type headers require an x-match header(541)
    rxheaders = session.receiver("""match-q;{create: always
                                            , node: {type: queue}
                                            , link: { x-bindings:[{key: 'basic-labor'
                                                                , exchange: 'amq.match'
                                                                , queue: 'match-q'
                                                                , arguments:{'x-match': 'any', 'basic-labor': 1}
                                                                },
                                                                {key: 'basic-premium-labor'
                                                                , exchange: 'amq.match'
                                                                , queue: 'match-q'
                                                                , arguments:{'x-match': 'all', 'basic-labor': 1, 'premium-labor': 1}
                                                                }]
                                                    }
                                            }"""
                                 )
    
    
    sender.send(Message(json.dumps({"1" : "apple", "2" : "bananan"})
                            , properties={'basic-labor': 1, 'premium-labor': 1}
                            ,  id = "aaaaaaaaaaaaa"))
    
    
    
    message = rxheaders.fetch(timeout=1)  #(5)
    print (message.content, "received")
    print(rxheaders.available())
    session.acknowledge() #(6)

except MessagingError as m:
    print (m)
finally:
    connection.close()  #(7)