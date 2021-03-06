# Brick_1.py
import bluetooth
import sys
from threading import Thread
from time import sleep

from DSLFunctions import DSLFunctions
from MovementController import MovementController
from Utils import Utils

sys.path.append('../src-gen')
from MissionList import MissionList  # The unresolved import error generated here by Eclipse should be ignored.

server_mac = 'CC:78:AB:50:B2:46'

def main():   
    # Setup bluetooth connection with slave, and sensor communications
    sock, sock_in, sock_out = connect()
    utils = Utils(1, sock_out)
    
    listener = Thread(target=listen, args=(sock_in, sock_out, utils))
    listener.start()
    
    # Setup internal control systems
    mContr = MovementController(utils) 
    dsl = DSLFunctions(mContr, utils)
    missions = MissionList(dsl).getMissionSet()
    #print(missions)
    
    sleep(1) # make sure that the sensors have had an opportunity to get started
    utils.updateSensorVals(quick = False)
    
    # Mission Execution Loop
    for missionName, mission in missions.items():
        if utils.shouldStop:
            break
        print('Started doing mission "' + missionName + '"')
        for movement in mission:
            if utils.shouldStop:
                break
            utils.resetTracker()
            for action in movement["moves"]:
                utils.updateSensorVals()
                sleep(0.5) # allow sensors from brick 2 some time to update
                
                if utils.shouldStop:
                    break
                action(movement["conditions"])
    
    utils.shouldStop = True
     
    sock_out.write("{'stop': True}\n") # Notify the slave of stop
    sock_out.flush()
    
    listener.join() # waits for stop acknowledge from slave
    
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
    while not utils.shouldStop:
        data = sock_in.readline()
        if data.strip() != "": # checks if the line is empty or just containing whitespace
            #print('MASTER: Received bt message:')
            #print(data, end="")
            data = eval(data)
            
            
            if data["stop"]:
                print('MASTER: Received last message, quitting')
                utils.shouldStop = True
                break
            else:
                utils.lastTouchL = data["touchL"]
                utils.lastTouchR = data["touchR"]
                utils.lastTouchB = data["touchB"]
                utils.lastDistF = data["distF"]
                
                if not utils.shouldStop: 
                    #sleep(1)
                    utils.updateSensorVals(quick = False)
    
main()