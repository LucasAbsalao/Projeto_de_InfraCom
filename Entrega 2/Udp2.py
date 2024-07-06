from pathlib import Path
import socket as skt
import time

class socketUdp():

    def __init__(self, endereco, porta, Max_Buff):
        self.Max_Buff = Max_Buff
        self.sckt = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        self.sckt.bind((endereco, porta))
        self.sckt.settimeout(1)  # Timeout configurado para 1 segundo
        
        if self.sckt is None:
            raise "Socket not available."

    #============================================================================================

    def sendMsg(self, server_addr: tuple[str, int], msg: bytes):   #Enviar "mensagem"
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)

    def recMsg(self):   #Receber "mensagem"
        try:
            data, origin = self.sckt.recvfrom(self.Max_Buff)
            return data, origin
        except:
            return b'\xFF', "Null"      # Caso não receba mensagem retorne "11111111"

    #============================================================================================

    def rdtSend(self, server_addr: tuple[str, int], msg: bytes, seq: int):  #Ao ser chamado envia a mensagem e aguarda uma confirmação
        count = 2  # Número máximo de tentativas

        while count > 0:
            self.sendMsg(server_addr, seq.to_bytes(1, 'big') + msg)  # Concatena o número de sequência ao início da mensagem

            try:
                ans, origin = self.recMsg()  # Espera pela confirmação
                if ans[0] == seq:
                    break  # Confirmação recebida
            except:
                count -= 1  # Timeout, reduz o contador e tenta novamente

    def rdtRcv(self, expected_seq: int):
        while True:
            data, origin = self.recMsg()
            if data[0] == expected_seq:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, expected_seq.to_bytes(1, 'big'))
                return data[1:], origin  # Retorna os dados sem o número de sequência
            else:
                # Retransmite o último ACK para sinalizar o remetente
                self.sendMsg(origin, (1 - expected_seq).to_bytes(1, 'big'))

    #============================================================================================

    def send_file(self, name_file: str, server_addr: tuple[str, int]):
        with open(name_file, "rb") as f:
            data = f.read()

        packets = []
        j = k = 0
        packets.append(bytearray())

        # Quebrando o arquivo em pacotes de tamanho Max_Buff-1
        for i in data:
            if j < (self.Max_Buff - 1):   # Menos 1 porque é o tamanho do cabeçalho
                packets[k].append(i)
                j += 1
            else:
                j = 1
                k += 1
                packets.append(bytearray())
                packets[k].append(i)

        print('Enviando arquivo')

        # Enviando cada um dos pacotes com alternância de sequência 0 e 1
        seq = 0
        for packet in packets:
            self.rdtSend(server_addr, packet, seq)
            seq = 1 - seq  # Alterna entre 0 e 1

        # Enviando um sinal de tchau para o server parar de ouvir quando receber o arquivo inteiro
        while True:
            self.sendMsg(server_addr, b'\x03')
            ans, origin = self.recMsg()
            if ans[0] == 3:
                break

        print('Arquivo totalmente enviado!')
        self.sckt.close()

    def listen_file(self, name_file):
        print('Recebendo arquivo')
        storage = bytearray()

        expected_seq = 0
        while True:
            data, origin = self.rdtRcv(expected_seq)
            if data[0] == 3:  # Mensagem de tchau
                self.sckt.close()
                break
            else:
                storage += data
                expected_seq = 1 - expected_seq  # Alterna entre 0 e 1

        # Remontando o arquivo
        new_file = Path(name_file)
        with new_file.open('wb') as file:
            file.write(storage)

        print('Arquivo (supostamente) recebido com sucesso!')

#============================================================================================
