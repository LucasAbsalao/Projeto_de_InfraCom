from pathlib import Path
import socket as skt
import time

class Client():

    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)
        self.storage = []

        if self.sckt is None:
            raise "Socket not available."

        self.MAX_BUFF = MAX_BUFF

    def listen(self, server_addr: tuple[str, int]):
        while True:
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
                if data.decode() == "STOP":
                    self.send(server_addr, "Saindo".encode())
                    self.sckt.close()
                    break
                elif data.decode() == "PAUSE":
                    break
                else:
                    self.storage.append(data)
                    print("PACOTE RECEBIDO NO CLIENTE!")
            except:
                continue

    def send(self, server_addr: tuple[str, int], msg: bytes):
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)
        print("PACOTE ENVIADO PELO CLIENTE!")

    def send_file(self, name_file: str, server_addr: tuple[str, int]):

        f = open(name_file, "r")
        text = f.read()
        text_b = text.encode()
        f.close()

        packets = []
        j = k = 0
        packets.append(bytearray())

        # Quebrando o arquivo em pacotes de 1024 Bytes

        for i in text_b:
            if j < self.MAX_BUFF:
                packets[k].append(i)
                j += 1
            else:
                j = 0
                k += 1
                packets.append(bytearray())

        # Enviando cada um dos pacotes
        for i in packets:
            self.send(server_addr, i)

        # Enviando um sinal de pausa para o server parar de ouvir quando receber o arquivo inteiro
        self.send(server_addr, "PAUSE".encode())

    def listen_file(self, name_file, addr_bind, ):
        self.listen(addr_bind)

        # remontando o arquivo

        new_file = Path(name_file)
        text = ""
        for i in self.storage:
            text += i.decode()

        new_file.write_text(text)

    def close(self):
        self.sckt.close()





