from pathlib import Path
import socket as skt
import time, random


class socketUdp():

    def __init__(self, endereco, porta, Max_Buff):
        self.Max_Buff = Max_Buff
        self.sckt = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        self.sckt.bind((endereco, porta))
        self.sckt.settimeout(1)  # Timeout configurado para 1 segundo
        self.clients={}
        self.accomodations ={}
        self.reservas= {}
        self.seqNumber = 1
        self.numRsv = 0


        if self.sckt is None:
            raise "Socket not available."

    # ============================================================================================

    def allOperations(self, adress, data):
        message= data.decode()
        command, *other_commands= message.split()


        if command =="login":
            self.lo
        ## isso tá errado

    def login(self, username,clientID,server_addr):
        print("entrou no login")
        flag=True
        for cliente in self.clients.values():
            print(cliente[0])
            if(cliente[0]==username):
                if(cliente[2]==True):
                    self.rdtSend(server_addr, b'\xFF' + "Usuario já está online".encode())
                else:
                    cliente[2]=True
                    cliente[3]=server_addr
                    self.rdtSend(server_addr,cliente[1].to_bytes(1,'big')+"Usuario ".encode())
                flag=False
                break

        if(flag):
            self.clients[clientID]=[username, clientID, True, server_addr]
            self.rdtSend(server_addr,clientID.to_bytes(1,'big')+"Usuario cadastrado".encode())
            return 1
        return 0

    '''def login(self, username,clientID,server_addr):
        print("entrou no login")
        flagUsername=True
        flagIP=True
        for cliente in self.clients.values():
            print(cliente[0])
            if(cliente[0]==username):
                self.rdtSend(server_addr, clientID.to_bytes(1,'big')+"Usuario ja presente na lista".encode())
                flagUsername=False

        for clienteID in self.clients.values(): #Mudar o username desse cliente
            if server_addr == clienteID[2]:
                self.rdtSend(server_addr, clienteID[1].to_bytes(1,'big')+"Username do client foi trocado".encode())
                print(clienteID[2])
                clienteID[0] = username
                flagIP=False

        if flagUsername==True and flagIP == True:
            self.clients[clientID]= [username, clientID, server_addr]
            self.rdtSend(server_addr,clientID.to_bytes(1,'big')+"Usuario cadastrado".encode())
            return 1
        else: return 0'''

    def logout(self, clientID, server_addr):
        username = self.get_username(clientID)
        if username!= None:
            self.clients[clientID][2]=False
            self.rdtSend(server_addr, "Usuario desconectado".encode())
        else:
            self.rdtSend(server_addr, "Usuario não encontrado".encode())

    def get_username(self, clientID):
        for cliente in self.clients.values():
            if cliente[1] == clientID:
                return cliente[0]
        return None

    def cancel(self, clientID, accomodationID, date, server_addr):
        print("Iniciando Cancelamento")
        name = self.clients[clientID][0]
        flag = False
        for rsv in self.reservas.items():
            if (rsv[1][1]==int(accomodationID) and rsv[1][3]==name and rsv[1][2]==date):
                del self.reservas[rsv[0]]
                flag = True
                break
        if(flag):
            msg = name + "/" + str(server_addr[0]) + str(server_addr[1]) + "\n A reserva da acomodação" + str(accomodationID) + "na data" + str(date) + "foi cancelada!"
            print(msg)
        else:
            msg = "Reserva não Encontrada"
            print(msg)

    
    def createAccomodations(self,accomodationsData,clientID, accomodationID,server_addr):
        accomodationName=""
        accomodationLocal= ""
        accomodationInfo = ""

        flag=0
        for letter in accomodationsData:
            if(letter!='#'):
                if(flag==0):
                    accomodationName+=letter
                elif(flag==1):
                    accomodationLocal+=letter
                elif(flag==2):
                    accomodationInfo+=letter
            else:
                flag+=1

        aux=True
        for accomodation in self.accomodations.values():
            if(accomodationName==accomodation[0] and accomodationLocal==accomodation[1]):
                self.rdtSend(server_addr, "acomodação já foi criada".encode())
                aux = False

        if(aux):
            self.accomodations[accomodationID]=[accomodationName,accomodationLocal,accomodationInfo, clientID]
            self.rdtSend(server_addr, ("acomodação de nome : " + accomodationName + " " + "foi criada com sucesso").encode())
            #for clientes in self.clients.values():
                #if clientes[1]!=clientID:
                    #self.rdtSend(server_addr, ("["+clientes[0]+"/"+str(clientes[2])+"]" + "acomodação de nome e localização: "+accomodationName+" "+accomodationLocal+"foi criado pelo cliente "+ str(clientID)).encode())
            return 1

        else:
            return 0

        
    def listMyRsv(self, server_addr, userID):
        msg = ""
        for reserva in self.reservas.values():
            if (reserva[0] == userID):
                msg += (self.accomodations[reserva[1]][0] + " - Data: " + str(reserva[2][0]) + "/" + str(reserva[2][1]) + "/" + str(reserva[2][2]) +"\n")
        self.rdtSend(server_addr, msg.encode())
    
    def listAcmd(self, server_addr):
        msg = ""
        for index, accomodation in enumerate(self.accomodations.values()):
            msg += ("(" + str(index) + ") " +accomodation[0] + ", " + accomodation[2] + ", Local: " + accomodation[1] +  "\n")
        self.rdtSend(server_addr, msg.encode())

    def book(self, server_addr, msg):
        idClt = msg[1] 
        idAcmd = msg[2]
        dia = msg[3]
        mes = msg[4]
        ano = msg[5] + 2000
        nome = msg[6:].decode()
        
        flag=True
        for reserva in self.reservas.values():
            if(idAcmd == reserva[1]):
                if((dia,mes,ano) == reserva[2]):
                    flag = False
                    break
        if(flag):
            self.reservas[self.numRsv] = [idClt, idAcmd, (dia,mes,ano), nome]
            self.numRsv += 1
            self.rdtSend(server_addr, "Sua reserva está confirmada".encode())
        else:
            self.rdtSend(server_addr, "Não foi possível realizar sua reserva, verifique os dados e tente novamente".encode())

     # ============================================================================================
    def sendMsg(self, server_addr: tuple[str, int], msg: bytes):  # Enviar "mensagem"
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)

    def recMsg(self):  # Receber "mensagem"
        try:
            data, origin = self.sckt.recvfrom(self.Max_Buff)
            return data, origin
        except:
            #print("tempo de requisição expirado")
            return b'\xFF', "Null"  # Caso não receba mensagem retorne "11111111"

    # ============================================================================================

   
    def rdtSend(self, server_addr: tuple[str, int], msg: bytes):  # Ao ser chamado envia a mensagem e aguarda uma confirmação

        self.seqNumber = 1 - self.seqNumber 

        while True:
            self.sendMsg(server_addr, (self.seqNumber).to_bytes() + msg)  # Concatena o número de sequência ao início da mensagem
            #print("Remetente: enviando seq ", self.seqNumber, "\nEsperando confirmação")

            ans, origin = self.recMsg()  # Espera pela confirmação

            #print("Cliente: ", ans[0])
            if ans[0] == self.seqNumber:
                #print("Remetente: Ack recebido ", self.seqNumber)
                break  # Confirmação recebida
            # if ans[0] == 255:
            #    print("Timeout!\nPronto para reenviar")
            #else:
             #   print("Número de sequência errado, reenviar")

    def rdtRcv(self):

        self.seqNumber = 1 - self.seqNumber 

        while True:

            data, origin = self.recMsg()

            if data[0] == self.seqNumber:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, (self.seqNumber).to_bytes(1, 'big'))
                #print("Destinatário: pacote recebido com sucesso\nEnviando ack: ", self.seqNumber)
                return data[1:], origin  # Retorna os dados sem o número de sequência
            else:
                # Retransmite o último ACK para sinalizar o remetente
                if (origin != "Null"):
                    #print("Destinatário: pacote recebido com erro\nEnviando ack anterior: ", 1 - self.seqNumber)
                    self.sendMsg(origin, (1 - self.seqNumber).to_bytes(1, 'big'))

    # ============================================================================================



