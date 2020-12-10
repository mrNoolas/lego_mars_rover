# Brick_2.py

from Utils import Utils
import bluetooth

server_mac = 'CC:78:AB:50:B2:46'

def main():    
    # start bluetooth sockets
    sock, sock_in, sock_out = connect()
    utils = Utils(2)
    
    print('SLAVE: Now listening...')
    while not utils.isDone:
        data = sock_in.readline()
        if data.strip() != "": # checks if the line is empty or just containing whitespace
            data = eval(data)
                        
            if data["stop"]:
                print('SLAVE: Received full stop, quitting')
                utils.isDone = True
                sock_out.write("{'stop': True}\n") # confirm stop to master
                sock_out.flush()
            elif data["dataRequest"]:
                utils.updateSensorVals()
                
                data = "{'stop': False, "
                data += "'touchL': " + str(bool(utils.lastTouchL)) + ", 'touchR': " + str(bool(utils.lastTouchR)) 
                data += ", 'touchB': " + str(bool(utils.lastTouchB)) + ", 'distF': " + str(utils.lastDistF)
                data += "}\n"
                
                print('SLAVE: Got data request. Sending the following data:')
                print(data, end="")
                sock_out.write(data)
                sock_out.flush()
    
    print("Shutting down.")
    sock_out.close()
    sock_in.close()
    sock.close()
    return 0
    
def connect():
    port = 3
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('SLAVE: Connecting...')
    sock.connect((server_mac, port)) 
    print('SLAVE: Connected to ', server_mac)
    return sock, sock.makefile('r'), sock.makefile('w') 
    
    
main()