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
        self.bufferSeq=[]
        self.numRsv = 0


        if self.sckt is None:
            raise "Socket not available."

    # ============================================================================================

    def numSeq(self, addr, flag):
        for end in self.bufferSeq:
            if addr == end[0]:
                temp = end[1]
                if(flag==True):
                    end[1]= 1 - end[1]
                return temp

        self.bufferSeq.append([addr,0])
        return 0

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
            idCreator = self.accomodations[int(accomodationID)][3]
            creator = self.clients[idCreator]
            msg = " A reserva da acomodação " + str(accomodationID) + " na data " + str(date) + " foi cancelada!"
            msg2 = "[" + creator[0] + "/" + str(creator[3]) + "] novas disponibilidades para a acomodação " + self.accomodations[int(accomodationID)][0] + " " + self.accomodations[int(accomodationID)][1] + " " +self.accomodations[int(accomodationID)][2]
            msg3 = "[" + name + "/" + str(server_addr[0]) + ", " + str(server_addr[1]) + "] cancelou a reserva na sua acomodacao " + self.accomodations[int(accomodationID)][0] + " na data " + str(date)

            self.rdtSend((creator[3][0], creator[3][1]+1), msg3.encode())
            for clientes in self.clients.values():
                if(clientes[1]!=creator[1] and clientes[2]==True):
                    self.rdtSend((clientes[3][0],clientes[3][1]+1), msg2.encode())
        else:
            msg ="[" + name + "/" +  str(server_addr[0]) + str(server_addr[1]) + "]" + " Reserva não Encontrada!"
        return msg

    
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
            for clientes in self.clients.values():
                if clientes[1]!=clientID and clientes[2] == True:
                    self.rdtSend((clientes[3][0],clientes[3][1]+1), ("["+self.clients[clientID][0]+"/"+str(self.clients[clientID][3])+"]" + " acomodação de nome e localização: "+accomodationName+" "+accomodationLocal+" foi criado pelo cliente "+ str(clientID)).encode())
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

    def listMyAcmd(self, clientID, server_addr):
        msg = ""
        for index, acm in enumerate(self.accomodations.values()):
            if (acm[3]) == int(clientID):
                msg += ("(" + str(index) + ") " + acm[0] + ", " + acm[2] + ", Local: " + acm[1] + "\n")
                msg += "Reservas dessa acomodação: \n"
                for rsv in self.reservas.values():
                    if(rsv[1] == index):
                        msg += "Por " + str(rsv[3]) + "(" + str(self.clients[rsv[0]][3]) + ")" + " na data " + str(rsv[2]) + "\n"
        return msg

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
            if (idClt != self.accomodations[idAcmd][3]):
                self.reservas[self.numRsv] = [idClt, idAcmd, (dia,mes,ano), nome]
                self.numRsv += 1
                self.rdtSend(server_addr, "Sua reserva está confirmada".encode())
                acmdCreator = self.clients[self.accomodations[idAcmd][3]]
                msg = "[" + self.clients[idClt][0] + "/" + str(self.clients[idClt][3]) + "] reservou a acomodacao " + self.accomodations[idAcmd][0]
                self.rdtSend((acmdCreator[3][0], acmdCreator[3][1] + 1), msg.encode())

            else:
                self.rdtSend(server_addr,"Não é possível reservar sua própria acomodação!".encode())
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
            return b'\xFF', None  # Caso não receba mensagem retorne "11111111"

    # ============================================================================================

   
    def rdtSend(self, server_addr: tuple[str, int], msg: bytes):  # Ao ser chamado envia a mensagem e aguarda uma confirmação


        while True:
            
            seqNumber = self.numSeq(server_addr, False)

            self.sendMsg(server_addr, (seqNumber).to_bytes() + msg)  # Concatena o número de sequência ao início da mensagem
            #print("Remetente: enviando seq ", seqNumber, "\nEsperando confirmação")

            ans, origin = self.recMsg()  # Espera pela confirmação

            #print("Cliente: ", ans[0])
            if ans[0] == seqNumber:
                #print("Remetente: Ack recebido ", seqNumber)
                self.numSeq(server_addr,True)
                break  # Confirmação recebida
            # if ans[0] == 255:
            #    print("Timeout!\nPronto para reenviar")
            #else:
             #   print("Número de sequência errado, reenviar")

    def rdtRcv(self):

        while True:

            data, origin = self.recMsg()
            seqNumber = self.numSeq(origin, False)
            
            if data[0] == seqNumber:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, (seqNumber).to_bytes(1, 'big'))
                #print("Destinatário: pacote recebido com sucesso\nEnviando ack: ", seqNumber)
                self.numSeq(origin,True)
                return data[1:], origin  # Retorna os dados sem o número de sequência
            else:
                # Retransmite o último ACK para sinalizar o remetente
                if (origin != None):
                    #print("Destinatário: pacote recebido com erro\nEnviando ack anterior: ", 1 - seqNumber)
                    self.sendMsg(origin, (1 - seqNumber).to_bytes(1, 'big'))

    def rdtRcv2(self):

        while True:

            data, origin = self.recMsg()
            seqNumber = self.numSeq(origin, False)
            
            if data[0] == seqNumber:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, (seqNumber).to_bytes(1, 'big'))
                #print("Destinatário: pacote recebido com sucesso\nEnviando ack: ", seqNumber)
                self.numSeq(origin,True)
                return data[1:], origin  # Retorna os dados sem o número de sequência
            else:
                # Retransmite o último ACK para sinalizar o remetente
                if (origin != None):
                    #print("Destinatário: pacote recebido com erro\nEnviando ack anterior: ", 1 - seqNumber)
                    self.sendMsg(origin, (1 - seqNumber).to_bytes(1, 'big'))
                    return data, origin


    # ============================================================================================



