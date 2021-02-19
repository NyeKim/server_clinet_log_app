##  FILE : server.py
##  PROJECT : SENG2040 - Assignment #3
##  PROGRAMMER : Eunhye Kim
##  FIRST VERSION : 2020-11-15
##  DESCRIPTION : This is a network based python logging service(program).
##  This service handles client connections, messages, disconnections, and
##  other exceptions and errors. All of the events in this service are saved 
##  in a text file as logging information.



from socket import *
import threading
import time
import logging
import logging.handlers
import os
import sys
from datetime import datetime



##  FUNCTION :setLogfile 
##  DESCRIPTION : This file sets a log file name with the current date.
##                It follows a month-date-year-logfile.txt format.
##  PARAMETERS : No Parameters
##  RETURNS : logFileName: Set log file name
def setLogfile():
   
    logFileName= datetime.now().strftime("%m-%d-%Y")+'-logfile.txt'   

    return logFileName

   
##  FUNCTION : setLogger
##  DESCRIPTION : This function creates a logger for this service, sets the logging level,
##                sets the logging format, and sets a text file for logging information. 
##  PARAMETERS : filename : Set Log file name
##  RETURNS : myLogger: A logger of this service
def setLogger(filename):

    myLogger = logging.getLogger("server")
    myLogger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - "%(message)s"')

    #Set a logging format.
    streamHander = logging.StreamHandler()
    streamHander.setFormatter(formatter)
    myLogger.addHandler(streamHander)

    #Set a text file for logging information.
    fileHandler = logging.FileHandler(filename)
    fileHandler.setFormatter(formatter)
    myLogger.addHandler(fileHandler)

    return myLogger


##  FUNCTION : receive
##  DESCRIPTION : This function receives a message from the client by socket.
##                It saves the client message into the log file.
##  PARAMETERS : sock : client connection socket
##               myLogger: the service logger
##  RETURNS : No Returns
def receive(sock,myLogger):


    while True:
        

        recvData = sock.recv(1024)
        msg = recvData.decode('utf-8')
        msg = 'Received from the client:' + msg
        myLogger.info(msg)

        

   
##  FUNCTION : buildConnection
##  DESCRIPTION : This function executes/sets the service to get a connection
##                with a client.  
##  PARAMETERS : No Parameters
##  RETURNS : connectionSock : Connection socket of a client
def buildConnection():

       ##port=int(sys.argv[1])
    port=8081

    serverSock = socket(AF_INET,SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)

    connectionSock, addr = serverSock.accept()
    if True:
        msg = 'IP: ' + str(addr[0]) + ' is connected to the server.'
        myLogger.info(msg)
        if input("\nAre you accept the connection? if not, enter n to turn off the sever. If not, hit the enter.\n").lower().startswith('n'):
            myLogger.info('Turn off the Server gracefully.')
            sys.exit(1)    

    return connectionSock


##  FUNCTION : receiveBuilder
##  DESCRIPTION : This function builds a connection with a client 
##                and keeps listening messages from the client.
##                It catches a connection error(client disconnection).
##  PARAMETERS : myLogger : A logger of this service
##  RETURNS : No returns
def receiveBuilder(myLogger):

    
    try:
        
        connectionSock = buildConnection()
        receive(connectionSock,myLogger)
        
    ##when a client got disconnected from the server.
    except ConnectionResetError as err:
        
        myLogger.error('The client disconnected from the server.')
        connectionSock.close()
        #restart the function to keep building another connection.
        receiveBuilder(myLogger)



    
#service main()
if __name__ == '__main__':
    
    
    logfile = setLogfile()
    myLogger = setLogger(logfile)
    myLogger.info('Turn on the server.')

    try:

        receiveBuilder(myLogger)

       
    except KeyboardInterrupt:

        myLogger.fatal('Turn off the server.')
        sys.exit()




