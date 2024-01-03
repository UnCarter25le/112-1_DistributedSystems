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
    #codes below is key. It needs ceceiver to have clear binding and subscribe match queue or it won't receive any msg in amq.match exchange sent by sender/
    rxheaders = session.receiver("""match-q;{create: always
                                            , node: {type: queue}
                                            , link: { 
                                            x-bindings:[{key: 'binding-name-1'
                                                                , exchange: 'amq.match'
                                                                , queue: 'match-q'
                                                                , arguments:{'x-match': 'any', '1': 'apple', '2': 'banana'}
                                                                },
                                                                {key: 'binding-name-2'
                                                                , exchange: 'amq.match'
                                                                , queue: 'match-q'
                                                                , arguments:{'x-match': 'all', '1': 'apple', '2': 'banana', '3': 'orange'}
                                                                }]
                                                    }
                                            }"""
                                 )
    
    headers = {'x-match': 'all', '1': 'apple', '2': 'banana', '3': 'orange'}
    sender.send(Message(json.dumps({"1" : "apple", "2" : "banana"})
                            , properties=headers
                            ,  id = "3" if len(headers) == 3 else str(len(headers)) ))

    message = rxheaders.fetch(timeout=1)  #(5)
    print (message.content, message.id, "received")
    session.acknowledge() #(6)

except MessagingError as m:
    print (m)
finally:
    connection.close()  #(7)