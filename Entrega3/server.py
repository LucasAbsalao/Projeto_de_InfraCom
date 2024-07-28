import Udp


socket0 = Udp.socketUdp("127.0.0.1", 5557, 1024)
index=0

while True:

    data, origin = socket0.rdtRcv();
    print(data)

    if(data[0] == 0):   #login
        print( data[1:].decode(), "quer fazer login")
        socket0.login(data[1:].decode(),index,origin)
        index=index+1
        print(socket0.clients)
       ## socket0.rdtSend(origin, "Foi".encode())

    elif(data[0] == 1): #logout
        print(data[1:].decode(), "usuario saindo")
        socket0.logout(data[1:].decode(), origin)

    #elif(data[0] == 2):

    #elif(data[0] == 3):

    #elif(data[0] == 4):

    #elif(data[0] == 5):

    #elif(data[0] == 6):

    if(data[0] == 7): #logout
        print("saindo")
        break
