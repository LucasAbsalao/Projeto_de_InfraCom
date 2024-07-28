import Udp


addr = ('127.0.0.1',5557)
socket0 = Udp.socketUdp("127.0.0.1", 2424, 1024)

while True:

    comand = input()

    if (comand[0:6] == "login "):
        socket0.rdtSend(addr, b'\x00' + comand[6:].encode())
        data, origin = socket0.rdtRcv()
        print(data.decode())

    elif(comand[0:6]=="logout"):
        socket0.rdtSend(addr, b'\x01' + comand[6:].encode())
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