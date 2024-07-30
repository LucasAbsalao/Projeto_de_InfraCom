import Udp


socket0 = Udp.socketUdp("127.0.0.1", 5576, 1024)
indexCliente=0
indexAccomodation=0

while True:

    data, origin = socket0.rdtRcv()
    print(data)

    if(data[0] == 0):   #login
        print( data[1:].decode(), "quer fazer login")
        indexCliente=indexCliente+socket0.login(data[1:].decode(),indexCliente,origin)
       ## socket0.rdtSend(origin, "Foi".encode())

    elif(data[0] == 1): #logout
        print(data[1:].decode(), "usuario saindo")
        socket0.logout(data[1] ,origin)

    elif(data[0] == 2):#create
        print(data[1:].decode(), "quer criar acomodação")
        indexAccomodation = indexAccomodation + socket0.createAccomodations(data[2:].decode(),data[1], indexAccomodation,origin)

    elif(data[0] == 3):
        print(data[1], "pediu para listar")
        socket0.listMyRsv(origin,data[1])
    
    elif(data[0] == 4):
        print("pediu para listar")
        socket0.listAcmd(origin)

    elif(data[0] == 5):
        print("pedido de reserva")
        socket0.book(origin, data)

    elif(data[0] == 6):
        datas = data[2:].decode()
        datanf = datas[:8]
        dataf = (int(datanf[:2]), int(datanf[2:4]), int(datanf[4:]))
        print("pedido de cancelamento")
        msg = socket0.cancel(data[1], datas[8], dataf, origin)
        socket0.rdtSend(origin, msg.encode())

    elif(data[0] == 7):
        msg = socket0.listMyAcmd(data[1],origin)
        socket0.rdtSend(origin, msg.encode())


    print("Contas: ", socket0.clients)
    print("Acomodações: ", socket0.accomodations)
    print("Reservas: ", socket0.reservas)
