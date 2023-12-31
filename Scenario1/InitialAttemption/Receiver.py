from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time
import multiprocessing as mp
from threading import Thread
import threading
import sys

class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server, password="guest", user ="guest" )
        event.container.create_receiver(conn, "amq.topic/*")
        event.container.create_sender(conn, "amq.topic/*.*")

    def on_message(self, event):
        print(f"received：{event.message.body}")
        

        # event.connection.close()

    def on_sendable(self, event):
        event.sender.send(Message(body=f"Echo Hello World!"))
        print(f"sent：Echo Hello World!")
        event.sender.close()




exit_event = threading.Event()

def bb(PP):
    PP.run()




if __name__ ==  '__main__':

    try:
        
        a = Container(HelloWorld("localhost:5672", "amq.topic/1.2"))
        b = Container(HelloWorld("localhost:5672", "amq.topic/1.2"))
        

        print(a.container_id)

        t = Thread(target=bb, args=(a,))
        h = Thread(target=bb, args=(b,))
        t.daemon = True
        h.daemon = True        
        t.start()
        h.start()
        t.join()
        h.join()   
        
        """
        # reduction.py", line 79, in duplicate
        # return _winapi.DuplicateHandle(
        # PermissionError: [WinError 5] Access is denied
        """
        # b_proc = mp.Process(target=bb, args=(b,))
        # b_proc.daemon = True
        # b_proc.start()                
        
        print(b.container_id)

        
    
          
        
    except KeyboardInterrupt as e:
        
 
        b_proc.terminate()
        pass
    