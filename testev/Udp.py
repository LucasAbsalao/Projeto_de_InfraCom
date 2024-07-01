from pathlib import Path
import socket as skt
import time

class socketUdp():

    def __init__(self, endereco, porta, Max_Buff):
        self.Max_Buff = Max_Buff
        self.sckt = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        self.sckt.bind((endereco, porta))
        self.sckt.settimeout(5)
        
        if self.sckt is None:
            raise "Socket not available."

#============================================================================================

    def sendMsg(self, server_addr: tuple[str,str], msg: bytes):   #Enviar "mensagem"

        self.sckt.sendto(msg,server_addr)
        time.sleep(0.0001)

    def recMsg(self):   #Receber "mensagem"

        while True:
            try:
                data, origin = self.sckt.recvfrom(self.Max_Buff)
                if(data != None):
                    break
            except:
                data = b'\xFF'      #Caso não receba mensagem retorne "11111111"
                origin = "Null"
                break

        return data, origin

#============================================================================================

    def rdtSend(self, server_addr: tuple[str, str], msg: bytes):  #Ao ser chamado envia a mensagem e aguarda uma confirmação
       
        count = 2 #Controla o numero de mensagens que podem ser reenviadas até desistir de enviar, usado para testes

        while True:

            #print('Enviando mensagem!')
            
            self.sendMsg(server_addr, b'\x00' + msg)  #Envia a mensagem
            ans, origin = self.recMsg() #Recebe uma mensagem

            if(ans[0] == 1): #O primeiro byte deixei como cabeçalho, 1 representa um ack
                #print('Confirmação recebida')
                break

            else:
                count = count - 1
                #print('Confirmação não recebida! reenviar')
            
            if(count == 0):
                #print("Pacote não enviado!")
                break

    def rdtRcv(self):
        
        #print('Recebendo mensagem!')

        data, origin = self.recMsg()  #Recebe uma mensagem
        
        if(data[0] == 0):  #0 representa que é um dado, aqui deveria ter também a checagem de integridade
            #print('Enviando confirmação')
            self.sendMsg(origin, b'\x01')

        elif(data[0] == 3): #Para manter a compatibilidade, 3 fica sendo uma mensagem de tchau
            self.sendMsg(origin, b'\x03')

        #else:
            #self.sendMsg(origin, b'\x02')

        return data

#============================================================================================

    def send_file(self, name_file: str, server_addr: tuple[str, int]):

        f = open(name_file, "rb")
        data = f.read()
        f.close()

        packets = []
        j = k = 0
        packets.append(bytearray())

        # Quebrando o arquivo em pacotes de 1024 Bytes

        for i in data:
            if j < (self.Max_Buff-1):   #Menos 1 porque é o tamanho do cabeçalho
                packets[k].append(i)
                j += 1
            else:
                j = 1
                k += 1
                packets.append(bytearray())
                packets[k].append(i)

        print('Enviando arquivo')

        # Enviando cada um dos pacotes
        for i in packets:
            self.rdtSend(server_addr, i)

        # Enviando um sinal de tchau para o server parar de ouvir quando receber o arquivo inteiro
        count = 2

        while True:
            self.sendMsg(server_addr, b'\x03')
            ans, origin = self.recMsg()
            if(ans[0] == 3):
                break

            count = count -1
            if count == 0:
                break

        print('Arquivo totalmente enviado!')

        self.sckt.close()

    def listen_file(self, name_file):

        print('Recebendo arquivo')
        storage = bytearray()

        count = 2

        while True:
            try:
                data = self.rdtRcv()
                if (data[0] == 3):
                    #print('Identificou um tchau! Encerrando recebimento.')
                    self.sckt.close()
                    break
                elif(data[0] == 0):
                    storage += (data[1:])

                else:
                    count = count -1
                    if count == 0:
                        break
            
            except:
                continue

        #remontando o arquivo
        new_file = Path(name_file)

        with new_file.open('wb') as file:
            file.write(storage)

        print('Arquivo (supostamente) recebido com sucesso!')

#============================================================================================
