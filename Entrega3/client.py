import Udp


addr = ('127.0.0.1',5559)
socket0 = Udp.socketUdp("127.0.0.1", 2426, 1024)
auxID= 0

while True:

    comand = input()

    if (comand[0:6] == "login "):
        socket0.rdtSend(addr, b'\x00' + comand[6:].encode())
        data, origin = socket0.rdtRcv()
        print(data.decode())
        auxID=data[0] 
        print(auxID)

    elif(comand[0:6]=="logout"):
        socket0.rdtSend(addr, b'\x01' + comand[6:].encode())
        data, origin = socket0.rdtRcv()
        print(data.decode())

    elif (comand=="create"):
          accomodationName=input("Digite o nome da acomodação: ")
          accomodationLocal=input("Digite a localização da acomodação: ")
          accomodationAble= input("Digite a disponibilidade da acomodação: ")
          message=accomodationName + "#" + accomodationLocal + "#" + accomodationAble

          print(message)
          socket0.rdtSend(addr, b'\x02' + auxID.to_bytes(1, 'big') + message.encode())
          data, origin = socket0.rdtRcv()
          print(data.decode())


    elif (comand == "quit"):
        break

    elif (comand == "help"):
        print("Digite quit para sair")

    else:
        print("comando nÃ£o reconhecido")

    #socket0.rdtSend(addr, b'\x00' + nome.encode())
    #socket0.rdtSend(addr, b'\xFF')