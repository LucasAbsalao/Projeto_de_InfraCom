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
        self.seqNumber = 1


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
                self.rdtSend(server_addr, "Usuario ja presente na lista".encode())
                flag=False
        
        if(flag):
           self.clients[clientID]=[username, clientID]
           self.rdtSend(server_addr,clientID.to_bytes(1,'big')+"Usuario cadastrado".encode())

    def logout(self, username,clientID, server_addr):
        username = self.get_username(clientID)
        if username!= None:
            del self.clients[clientID-1]
            self.rdtSend(server_addr, "Usuario removido com sucesso".encode())
        else:
            self.rdtSend(server_addr, "Usuario não encontrado".encode())

    def get_username(self, clientID):
        for cliente in self.clients.values():
            if cliente[1] == clientID:
                return cliente[0]
        return None
    
    def createAccomodations(self,accomodationsInfo,clientID, accomodationID,server_addr):
        accomodationName=""
        accomodationLocal= ""
        accomodationAble=""
        flag=0
        for letter in accomodationsInfo:
            if(letter!='#'):
                if(flag==0):
                    accomodationName+=letter
                elif(flag==1):
                    accomodationLocal+=letter
                else:
                    accomodationAble+=letter
            else:
                flag+=1
        aux=True
        for accomodation in self.accomodations.values():
            if(accomodationName== accomodation[0]):
                self.rdtSend(server_addr, "acomodação já foi criada".encode())
                aux = False
        
        if(aux):
            self.accomodations[accomodationID]=[accomodationName,accomodationLocal,accomodationAble, clientID]
            self.rdtSend(server_addr, ("acomodação de nome : " + accomodationName + "foi criada com sucesso").encode())




        
    
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
            print("Remetente: enviando seq ", self.seqNumber, "\nEsperando confirmação")

            ans, origin = self.recMsg()  # Espera pela confirmação

            # print("Cliente: ", ans[0])
            if ans[0] == self.seqNumber:
                print("Remetente: Ack recebido ", self.seqNumber)
                break  # Confirmação recebida
            if ans[0] == 255:
                print("Timeout!\nPronto para reenviar")
            else:
                print("Número de sequência errado, reenviar")

    def rdtRcv(self):

        self.seqNumber = 1 - self.seqNumber 

        while True:

            data, origin = self.recMsg()

            if data[0] == self.seqNumber:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, (self.seqNumber).to_bytes(1, 'big'))
                print("Destinatário: pacote recebido com sucesso\nEnviando ack: ", self.seqNumber)
                return data[1:], origin  # Retorna os dados sem o número de sequência
            else:
                # Retransmite o último ACK para sinalizar o remetente
                if (origin != "Null"):
                    print("Destinatário: pacote recebido com erro\nEnviando ack anterior: ", 1 - self.seqNumber)
                    self.sendMsg(origin, (1 - self.seqNumber).to_bytes(1, 'big'))

    # ============================================================================================

    def send_file(self, name_file: str, server_addr: tuple[str, int]): #Envia o arquivo no path name_file

        with open(name_file, "rb") as f:
            data = f.read()
        f.close()

        packets = []
        j = k = 0
        packets.append(bytearray())

        # Quebrando o arquivo em pacotes de tamanho Max_Buff-1
        for i in data:
            if j < (self.Max_Buff - 1):  # Menos 1 porque é o tamanho do cabeçalho
                packets[k].append(i)
                j += 1
            else:
                j = 1
                k += 1
                packets.append(bytearray())
                packets[k].append(i)

        print('Enviando arquivo')

        # Enviando cada um dos pacotes com alternância de sequência 0 e 1
        numPacote = 0
        seq = 0
        for packet in packets:
            print("\nEnviando pacote: ", numPacote)
            numPacote += 1
            self.rdtSend(server_addr, packet, seq)
            seq = 1 - seq  # Alterna entre 0 e 1

        # Enviando um sinal de tchau para o server parar de ouvir quando receber o arquivo inteiro
        tries = 3
        bye_msg = 3
        while True:
            self.sendMsg(server_addr, bye_msg.to_bytes(1, 'big'))
            print("\nEnviando pacote: ", numPacote, "\nPedido de encerramento enviado")
            ans, origin = self.recMsg()
            if ans[0] == 3:
                print("Confirmação de fim recebida")
                break
            if tries == 0:
                break
            tries -= 1

        print("\nFim enviado")
        print('Arquivo totalmente enviado!')

    def listen_file(self, name_file): #Recebe o arquivo e o coloca no path de name_file

        self.endPoint = False
        print('Recebendo arquivo')

        storage = bytearray()

        numPacote = 0
        numPacoteConf = 0
        ack = 0
        while True:

            if(numPacote == numPacoteConf):
                print("\nRecebendo pacote: ", numPacote)
                numPacoteConf += 1

            data = self.rdtRcv(ack)

            if self.endPoint == True:  # Mensagem de tchau
                print("\nFim recebido")
                break
            elif data != b'':
                numPacote += 1
                storage += data
                ack = 1 - ack  # Troca o proximo ack

        # Remontando o arquivo
        new_file = Path(name_file)
        with new_file.open('wb') as file:
            file.write(storage)

        print('Arquivo (supostamente) recebido com sucesso!')

# ============================================================================================


