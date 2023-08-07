# NAME: Rudra Laxmi Kanth
# Roll Number: CS20B066
# Course: CS3205 Jan. 2023 semester
# Lab number: 2
# Date of submission:04-03-2023 
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): used LAB1 refernce


import socket
import os

localIP     = "127.0.0.1"
bufferSize  = 1024

print("Enter the value of K :")
k=int(input())   

print("Enter inputfile name :")
input_file=input()                                                #enter port number

def parse_input_file(input_file):
        with open(input_file, 'r') as f:                    #open inputfile
            lines = [line.strip() for line in f.readlines()]
            data = {}                                             # mapping ecah given data to ip
            data1 = {}                                            # mapping domains to ip
            current_list = None
            server = str()
            counter = 1
            for line in lines:
                elements = line.split()
                if len(elements) == 1:
                    server = elements[0][8:12]
                    current_list = None                           # reset current_list to None for non-list elements
                else:
                    #data[elements[0]] = elements[1]
                    values = elements[0].split('.')
                    if len(values)==2:
                        update = "ADS" + str(counter)
                        data[update] = elements[1]
                        counter = counter + 1               #diffrentiating ADS
                    else:
                        data[elements[0]] = elements[1] 
                    if len(values)==3:
                        data1[values[1]] = server                                                                 
                if current_list is not None and line == "END_DATA": # add the current_list to the data dictionary when a new list is encountered
                    data[current_list[0][0]] = current_list[1:]
        return data,data1                                        #returning data structures


new,new1=parse_input_file(input_file)

NR = open("NR.output","w")   #opening a file pointer
RDS = open("RDS.output","w") #opening a file pointer
TDS = open("TDS.output","w") #opening a file pointer
ADS = open("ADS.output","w") #opening a file pointer



def socket1():
   NRserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) #creating NR socket
   NRserversocket.bind(('localhost',k+53))
   clientportnumber = -1
   while(True):
        message,address=NRserversocket.recvfrom(bufferSize) #receving message
        message = message.decode()  
        if message=='-1':
              print("No DNS Record Found")            # if the given message is not in inputlist print the error
        elif message == 'kill':
            NRserversocket.sendto(message.encode(),('localhost',k+54))
            NRserversocket.close()                    #sending to RDS socket to close
            exit()
        if clientportnumber == -1:
            clientportnumber = address[1]             #saving initial clientport number
            NRserversocket.sendto(message.encode(),('localhost',k+54)) #sending to RDS socket
        else:
            kanthnew=message.split('/')
            if len(kanthnew) == 1:
                kanth1=kanthnew[0].encode()
                port=clientportnumber
                NRserversocket.sendto(kanth1,('localhost',port)) #sending to respective port after differntiating the message
                msgkaanth=message.split('/')
                if len(msgkaanth)==3:
                    a=1
                else:                                      #writing into NRfile
                    a=0
                NR.write("query: "+str(message)+" response sent: "+ str(msgkaanth[a])+" "+str(port)+'\n')
                clientportnumber = -1
            elif len(kanthnew) == 3:
                port=int(kanthnew[2])
                kanth1=kanthnew[0].encode()
                NRserversocket.sendto(kanth1,('localhost',port))
                msgkaanth=message.split('/')
                if len(msgkaanth)==3:
                    a=1
                else:                                    #writing into NRfile
                    a=0
                NR.write("query: "+str(message)+" response sent: "+str(msgkaanth[a])+" "+str(port)+'\n')

def socket2():
   RDSserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   RDSserversocket.bind(('localhost',k+54))    #creating RDS socket

   while(True):
        message,address=RDSserversocket.recvfrom(bufferSize)  #receving message from following socket
        temp = message.decode()
        message = temp.split('.')
        if temp =='kill':
            RDSserversocket.sendto(temp.encode(),('localhost',k+55)) #sending message to TDS1 for closing socket
            RDSserversocket.sendto(temp.encode(),('localhost',k+56)) #sending message to TDS2 for closing socket
            RDSserversocket.close()
            exit()
        if message[2]=="com":
           temp1=temp + '/' + new.get('TDS_com') + '/'+ str(k+55)
           kanth2=temp1.encode()
           RDSserversocket.sendto(kanth2,('localhost',k+53))  #sending back to NR socketwith adding ip to message
           msgkaanth=temp1.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                #writing into RDS file
                    a=0
           RDS.write("query: "+str(temp1)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        elif message[2]=="edu":
           temp1=temp + '/' + new.get('TDS_edu')+ '/'+ str(k+56)
           kanth2=temp1.encode()
           RDSserversocket.sendto(kanth2,('localhost',k+53))  #sending back to NR socketwith adding ip to message
           msgkaanth=temp1.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                               #writing into RDS file
                    a=0
           RDS.write("query: "+str(temp1)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        else :
           main=-1
           RDSserversocket.sendto(str(main).encode(),('localhost',k+53))
           msgkaanth=main                         #printing the error message if it is not belongs to avaliable domains
                                                  #here error message is "No DNS Record Found" same for all below
           RDS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(msgkaanth)+" "+str(k+53)+'\n')

def socket3():
   TDS1serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   TDS1serversocket.bind((localIP,k+55))  #creating TDS1 socket

   while(True):
        message,address=TDS1serversocket.recvfrom(bufferSize) #receving message from following socket
        message = message.decode()
        temp=message
        message = message.split('.')
        if temp == 'kill':
            TDS1serversocket.sendto(temp.encode(),('localhost',k+57)) #sending message to ADS11 for closing socket
            TDS1serversocket.sendto(temp.encode(),('localhost',k+58)) #sending message to ADS12 for closing socket
            TDS1serversocket.sendto(temp.encode(),('localhost',k+59)) #sending message to ADS13 for closing socket
            TDS1serversocket.close()
            exit()
        if new1.get(message[1])=="ADS1":
           temp=temp + '/' + new.get('ADS1')+ '/'+ str(k+57)
           kanth2=temp.encode()
           TDS1serversocket.sendto(kanth2,('localhost',k+53))    #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                       #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        elif new1.get(message[1])=="ADS2":
           temp=temp + '/' + new.get('ADS2')+ '/'+ str(k+58)
           kanth2=temp.encode()
           TDS1serversocket.sendto(kanth2,('localhost',k+53))   #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                         #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        elif new1.get(message[1])=="ADS3":
           temp=temp + '/' + new.get('ADS3')+ '/'+ str(k+59)
           kanth2=temp.encode()
           TDS1serversocket.sendto(kanth2,('localhost',k+53))  #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                         #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        else :
           main=-1
           TDS1serversocket.sendto(str(main).encode(),('localhost',k+53))
           msgkaanth=main                                       #printing the error message if it is not belongs to avaliable domains
           TDS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(msgkaanth)+" "+str(k+53)+'\n')

def socket4():
   TDS2serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   TDS2serversocket.bind((localIP,k+56)) #creating TDS2 socket

   while(True):
        message,address=TDS2serversocket.recvfrom(bufferSize)   #receving message from following socket
        message = message.decode()
        temp=message
        message = message.split('.')
        if temp == 'kill':
            TDS2serversocket.sendto(temp.encode(),('localhost',k+60))   #sending message to ADS21 for closing socket
            TDS2serversocket.sendto(temp.encode(),('localhost',k+61))   #sending message to ADS22 for closing socket
            TDS2serversocket.sendto(temp.encode(),('localhost',k+62))   #sending message to ADS23 for closing socket
            TDS2serversocket.close()
            exit()
        if new1.get(message[1])=="ADS4":
           temp=temp + '/' + new.get('ADS4')+ '/'+ str(k+60)
           kanth2=temp.encode()
           TDS2serversocket.sendto(kanth2,('localhost',k+53))  #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                            #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        elif new1.get(message[1])=="ADS5":
           temp=temp + '/' + new.get('ADS5')+ '/'+ str(k+61)
           kanth2=temp.encode()
           TDS2serversocket.sendto(kanth2,('localhost',k+53))   #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                            #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        elif new1.get(message[1])=="ADS6":
           temp=temp + '/' + new.get('ADS6')+ '/'+ str(k+62)
           kanth2=temp.encode()
           TDS2serversocket.sendto(kanth2,('localhost',k+53))  #sending back to NR socketwith adding ip to message
           msgkaanth=temp.split('/')
           if len(msgkaanth)==3:
                    a=1
           else:                                             #writing into TDS file
                    a=0
           TDS.write("query: "+str(temp)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
        else :
           main=-1
           TDS2serversocket.sendto(str(main).encode(),('localhost',k+53))
           msgkaanth=main                                    #printing the error message if it is not belongs to avaliable domains
           TDS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(msgkaanth)+" "+str(k+53)+'\n')

def socket5():
   ADS11serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS11serversocket.bind(('localhost',k+57)) #creating ADS11 socket

   while(True):
        message,address=ADS11serversocket.recvfrom(bufferSize)   #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS11serversocket.close()  # closing ADS11 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS11serversocket.sendto(str(temp).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else: 
            ADS11serversocket.sendto(str(new[message]).encode(),('localhost',k+53)) #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                          #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')

def socket6():
   ADS12serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS12serversocket.bind(('localhost',k+58))  #creating ADS12 socket

   while(True):
        message,address=ADS12serversocket.recvfrom(bufferSize)  #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS12serversocket.close()     # closing ADS12 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS12serversocket.sendto(str(temp).encode(),('localhost',k+53)) #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else: 
            ADS12serversocket.sendto(kanth2.encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                    #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')

def socket7():
   ADS13serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS13serversocket.bind(('localhost',k+59))  #creating ADS13 socket

   while(True):
        message,address=ADS13serversocket.recvfrom(bufferSize)   #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS13serversocket.close()      # closing ADS13 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS13serversocket.sendto(str(temp).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else: 
            ADS13serversocket.sendto(str(kanth2).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                    #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')

def socket8():
   ADS21serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS21serversocket.bind(('localhost',k+60))  #creating ADS21 socket

   while(True):
        message,address=ADS21serversocket.recvfrom(bufferSize)  #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS21serversocket.close()     # closing ADS21 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS21serversocket.sendto(str(temp).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else: 
            #print(kanth2)
            ADS21serversocket.sendto(kanth2.encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                    #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')
            

def socket9():
   ADS22serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS22serversocket.bind(('localhost',k+61))   #creating ADS22 socket

   while(True):
        message,address=ADS22serversocket.recvfrom(bufferSize)  #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS22serversocket.close()     # closing ADS22 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS22serversocket.sendto(str(temp).encode(),('localhost',k+53))   #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else: 
            ADS22serversocket.sendto(str(kanth2).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                        #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')

def socket10():
   ADS23serversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
   ADS23serversocket.bind((localIP,k+62))  #creating ADS23 socket

   while(True):
        message,address=ADS23serversocket.recvfrom(bufferSize) #receving message from following socket
        message = message.decode()
        kanth2=new.get(message)
        if message == 'kill':
            ADS23serversocket.close()      # closing ADS23 socket
            exit()
        if kanth2==None:
            temp=-1
            ADS23serversocket.sendto(str(temp).encode(),('localhost',k+53))   #sending back to NR socketwith adding ip to message
            ADS.write("query: "+str("No DNS Record Found")+" response sent: "+ str(temp)+" "+str(k+53)+'\n')
        else:          
            ADS23serversocket.sendto(str(kanth2).encode(),('localhost',k+53))  #sending back to NR socketwith adding ip to message
            msgkaanth=kanth2.split('/')
            if len(msgkaanth)==3:
                    a=1
            else:                  #writing into ADS file
                    a=0
            ADS.write("query: "+str(kanth2)+" response sent: "+ str(msgkaanth[a])+" "+str(k+53)+'\n')



for i in range(0,10):
    pid = os.fork()   #creating child processes and assiging to each iteration
    if pid==0:
        if i==0:
                socket1()
        elif i==1:
                socket2()
        elif i==2:
                socket3()
        elif i==3:
                socket4()
        elif i==4:
                socket5()
        elif i==5:
                socket6()
        elif i==6:
                socket7()
        elif i==7:
                socket8()
        elif i==8:
                socket9()
        elif i==9:
                socket10()
        exit()

#client DNS
serverAddressPort   = ("127.0.0.1", k+53)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #creating client socket

while True:
    print("Enter Server Name:")
    message=input()              #input domain name
    creator=message.split('.')
    if message == 'bye':
        bytestosend = 'kill'
        UDPClientSocket.sendto(bytestosend.encode(), serverAddressPort)   #sending to server 
        NR.close()            #closing files respectivly
        TDS.close()
        RDS.close()
        ADS.close() 
        print("All Server Processes are killed. Exiting.")   
        break 
    elif len(creator) !=3 :
         print("No DNS Record Found")           # given invalid input 
    else:  
        bytesToSend = str(message)
        UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort) #sending to server
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)            #receving from server
        msg = "DNS Mapping: {}".format(msgFromServer[0].decode())
        if msg!="DNS Mapping: -1":
             print(msg)                                                 #output
        