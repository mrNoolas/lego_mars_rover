# Brick_1.py

from Utils import Utils
from threading import Thread
from time import sleep
import bluetooth

server_mac = 'CC:78:AB:50:B2:46'

def main():
    #m = movement(u) 
    #move = doMovements(u,m)
    
    """ 
    behaviors has the fixed format [TODO: insert format ]
    """
    behaviors = []
    
    sock, sock_in, sock_out = connect()
    utils = Utils(1, sock_out)
    
    listener = Thread(target=listen, args=(sock_in, sock_out, utils))
    listener.start()
    
    #sender = Thread(target=send, args=(sock_in, sock_out, behaviors, utils))
    #sender.start()
    
    #Thread(target=go, args=[behaviors, utils]).start()
    #Thread(target=doAction, args=[behaviors, utils]).start()
    
    utils.updateSensorVals()
    
    while not utils.isDone:
        sleep(1)
        utils.isDone = True # TODO: remove Testing code
    
     
    sock_out.write("{'stop': True}\n") # Notify the slave of stop
    sock_out.flush()
    
    listener.join() # waits for stop acknowledge from slave
    #sender.join()
    
    print("Shutting down.") 
    sock_in.close()
    sock_out.close()
    sock.close()
    return 0
   
    
def connect():
    port = 3
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind((server_mac, port))
    server_sock.listen(1)
    
    print('MASTER: Listening...')
    client_sock, address = server_sock.accept()
    print('MASTER: Accepted connection from ', address)
    
    return client_sock, client_sock.makefile('r'), client_sock.makefile('w')    
    
    
def listen(sock_in, sock_out, utils):
    print('MASTER: Now listening...')
    while not utils.isDone:
        data = sock_in.readline()
        if data.strip() != "": # checks if the line is empty or just containing whitespace
            print('MASTER: Received bt message:')
            print(data, end="")
            data = eval(data)
            
            
            if data["stop"]:
                print('MASTER: Received last message, quitting')
                utils.isDone = True
                break
            else:
                utils.lastTouchL = data["touchL"]
                utils.lastTouchR = data["touchR"]
                utils.lastTouchB = data["touchB"]
                utils.lastDistF = data["distF"]

"""
    Handles the main execution using subsumption.
"""        
def go(behaviors, utils):
    activeBehavior = 0 #Standard = movement
    highest = 0 #Standard = movement
    behaviors[highest].active = True
    while not utils.isDone: 
        #print("MASTER: Current running behavior " + str(activeBehavior))
        #print("Colors to be checked:")
        #print(behaviors[1].colorsToFind)
        for i in range(len(behaviors)-1, -1, -1):
            if i > activeBehavior:
                if behaviors[i].takeControl() and behaviors[activeBehavior].active:
                    print("MASTER: Behavior " + str(i) + " wants to take control!")
                    print("MASTER: Suppressing behavior " + str(activeBehavior))
                    behaviors[activeBehavior].suppress()
                    print("MASTER: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
            elif not behaviors[activeBehavior].active:
                #No behavior is running, thus the highest can be started. 
                if behaviors[i].takeControl():
                    print("MASTER: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
        sleep(0.1)
         
"""
Performs actions given by 
"""
def doAction(behaviors, utils):
    while not utils.isDone:
        for i in range(len(behaviors)-1, -1, -1): 
            if behaviors[i].active:
                #print("MASTER: Thread runs behavior " + str(i))
                behaviors[i].action();
    
main()