import Udp, threading, time

myAddr = ("127.0.0.1", 7369)
addr = ('127.0.0.1',4890)

socket0 = Udp.socketUdp(myAddr[0], myAddr[1], 1024)
socket1 = Udp.socketUdp(myAddr[0], myAddr[1]+1, 1024)

auxID = 0
logged = False

def recieveMsg():
    while True:
        data, origin = socket1.rdtRcv2()
        if(origin != None):
            print("\n\nNotificação:\n" + data.decode() + "\n-----------------------------------------------")
        time.sleep(1)

threadRcv = threading.Thread(target=recieveMsg,daemon = True)
threadRcv.start()

while True:

    comand = input("> ")

    if (comand == "login"):
        if(logged):
            print("Você já está logado!")
        else:
            nome = input("Digite seu login: ")
            socket0.rdtSend(addr, b'\x00' + nome.encode())
            data, origin = socket0.rdtRcv()
            print(data[1:].decode())
            auxID=data[0]
            logged = True
            #print(auxID)

    elif(comand=="logout"):
        if(logged):
            socket0.rdtSend(addr, b'\x01' + auxID.to_bytes(1, 'big'))
            data, origin = socket0.rdtRcv()
            print(data.decode())
            logged = False
        else:
            print("Você não está logado!")

    elif (comand=="create"):

        if(logged):
            accomodationName=input("Digite o nome da acomodação: ")
            accomodationLocal=input("Digite a localização da acomodação: ")
            accomodationInfo= input("Digite informações da acomodação: ")
            message=accomodationName + "#" + accomodationLocal + "#" + accomodationInfo

            print(message)
            socket0.rdtSend(addr, b'\x02' + auxID.to_bytes(1, 'big') + message.encode())
            data, origin = socket0.rdtRcv()
            print(data.decode())
        else:
            print("Você precisa de uma conta para realizar a ação, faça login")
    
    elif(comand == "list:myrsv"):
        
        if(logged):
            socket0.rdtSend(addr, b'\x03' + auxID.to_bytes(1,'big'))
            data, origin = socket0.rdtRcv()
            print("Minhas reservas:\n", data.decode(), "-------------------")
        else:
            print("Você precisa de uma conta para realizar a ação, faça login")

    elif(comand == "list:acmd"):
        socket0.rdtSend(addr, b'\x04')
        data, origin = socket0.rdtRcv()
        print("Locais disponíveis:\n")
        print(data.decode())
        print("-------------------")

    elif(comand == "book"):

        if(logged):
            nome = input("Digite o nome do reservante: ")
            idAcmd = 0
            dia = 0
            mes = 0
            ano = 0 

            try:
                idAcmd = int(input("Digite o ID da acomodação: " ))
            
                while True:
                    try:
                        ano = int(input("Digite o ano da reserva: "))
                        if(ano > 2023 and ano < 2200):
                            break
                        else:
                            print("Esse ano já passou ou está muito longe, tente novamente")
                    except:
                        print("Tente novamente, digite apenas o número")

                while True:
                    try:
                        mes = int(input("Digite o mês da reserva: "))
                        if((mes > 0) and (mes < 13)):
                            break
                        else:
                            print("Mês inexistente, tente novamente")
                    except:
                        print("Tente novamente, digite apenas o número")

                while True:
                    try:
                        dia = int(input("Digite o dia da reserva: "))
                        if((dia > 0) and (dia < 32)):
                            break
                        else:
                           print("Dia inexistente, tente novamente")
                    except:
                        print("Tente novamente, digite apenas o número")
            except:
                print("O ID digitado não corresponde tente novamente, para conferir as acomodações disponíveis digite 'list:acmd'")
        
            socket0.rdtSend(addr, b'\x05' + auxID.to_bytes(1,'big') + idAcmd.to_bytes(1,'big') + dia.to_bytes(1,'big') + mes.to_bytes(1,'big') + (ano-2000).to_bytes(1,'big') + nome.encode())
            data, origin = socket0.rdtRcv()
            print(data.decode())

        else:
            print("Você precisa de uma conta para realizar a ação, faça login")

    elif (comand == "cancel"):
        if(logged):
            accomodationID = input("Digite o ID da acomodação: ")
            dia = input("Digite o dia da reserva: ")
            mes = input("Digite o mes da reserva: ")
            ano = input("Digite o ano da reserva: ")
            date = dia + mes + ano
            socket0.rdtSend(addr, b'\x06' + auxID.to_bytes(1, 'big') + date.encode() + accomodationID.encode())
            msg, _ = socket0.rdtRcv()
            msgs = msg.decode()
            print(msgs)

    elif (comand == "list:myacmd"):
        if (logged):
            socket0.rdtSend(addr, b'\x07' + auxID.to_bytes(1, 'big'))
            data, origin = socket0.rdtRcv()
            print("Minhas Acomodações:\n")
            print(data.decode())
            print("-------------------")

    elif (comand == "quit"):
        if(logged):
            socket0.rdtSend(addr, b'\x01' + auxID.to_bytes(1, 'big') )
            data, origin = socket0.rdtRcv()
            print(data.decode())
        break

    elif (comand == "help"):
        print("Comandos:\n 'quit' para sair\n 'login' para logar\n 'logout' para sair da conta\n 'list:acmd' para ver as acomodações disponíveis\n 'list:myrsv' para conferir suas reservas\n 'create' para anunciar uma acomodação\n 'book' para fazer uma reserva\n 'cancel' para cancelar reserva")

    else:
        print("comando não reconhecido, digite help por ajuda")

