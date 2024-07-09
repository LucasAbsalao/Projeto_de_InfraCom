from pathlib import Path
import socket as skt
import time, random


class socketUdp():

    def __init__(self, endereco, porta, Max_Buff):
        self.Max_Buff = Max_Buff
        self.sckt = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        self.sckt.bind((endereco, porta))
        self.sckt.settimeout(1)  # Timeout configurado para 1 segundo

        if self.sckt is None:
            raise "Socket not available."

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

    def rdtSend(self, server_addr: tuple[str, int], msg: bytes,seq: int):  # Ao ser chamado envia a mensagem e aguarda uma confirmação

        while True:
            self.sendMsg(server_addr, seq.to_bytes(1, 'big') + msg)  # Concatena o número de sequência ao início da mensagem
            print("Remetente: enviando seq ", seq, "\nEsperando confirmação")

            ans, origin = self.recMsg()  # Espera pela confirmação
            randomtimeout = random.uniform(0,1)  # Gera um número aleatório que será usado para simular a perda de um pacote
            # print("tempo: ", randomtimeout)
            if randomtimeout > 0.95:  # Gerador de perda aleatória de pacotes
                print("Injetando timeout: ", randomtimeout)
                ans[0] == 255
                continue

            # print("Cliente: ", ans[0])
            if ans[0] == seq:
                print("Remetente: Ack recebido ", seq)
                break  # Confirmação recebida
            if ans[0] == 255:
                print("Timeout!\nPronto para reenviar")
            else:
                print("Número de sequência errado, reenviar")

    def rdtRcv(self, expected_seq: int):
        while True:

            data, origin = self.recMsg()

            if data[0] == expected_seq:  # Número de sequência esperado
                # Envia a confirmação
                self.sendMsg(origin, expected_seq.to_bytes(1, 'big'))
                print("Destinatário: pacote recebido com sucesso\nEnviando ack: ", expected_seq)
                return data[1:]  # Retorna os dados sem o número de sequência
            elif data[0] == 3:
                print("Destinatário: Pedido de encerramento recebido")
                self.sendMsg(origin, b'\x03')
                print("Confirmação de fim enviada")
                self.endPoint = True
                return data
            else:
                # Retransmite o último ACK para sinalizar o remetente
                if (origin != "Null"):
                    print("Destinatário: pacote recebido com erro\nEnviando ack anterior: ", 1 - expected_seq)
                    self.sendMsg(origin, (1 - expected_seq).to_bytes(1, 'big'))
                return b''

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
        self.sckt.close()

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
                self.sckt.close()
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