from pathlib import Path
import socket as skt
import time

class Server():

    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)
        self.storage = []

        if self.sckt is None:
            raise "Socket not available."

        self.MAX_BUFF = MAX_BUFF

    def listen(self, name_file: str, server_addr: tuple[str, int]):
        f = open(name_file, "ab")
        while True:
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
                if str(data) == "b'STOP'":
                    self.send(server_addr, "Saindo".encode())
                    self.sckt.close()
                    break
                elif str(data) == "b'PAUSE'":
                    f.close()
                    break
                else:
                    #self.storage.append(data)
                    f.write(data)
                    print(self.storage)
                    print("PACOTE ARMAZENADO NO SERVIDOR!")
            except:
                continue

    def send(self, server_addr: tuple[str, int], msg: bytes):
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)
        print("PACOTE ENVIADO PELO SERVIDOR!")

    def send_file(self, name_file: str, server_addr: tuple[str, int]):

        f = open(name_file, "rb")
        data = f.read()
        f.close()

        packets = []
        j = k = 0
        packets.append(bytearray())

        # Quebrando o arquivo em pacotes de 1024 Bytes

        for i in data:
            if j < self.MAX_BUFF:
                packets[k].append(i)
                j += 1
            else:
                j = 1
                k += 1
                packets.append(bytearray())
                packets[k].append(i)

        # Enviando cada um dos pacotes
        for i in packets:
            self.send(server_addr, i)

        # Enviando um sinal de pausa para o server parar de ouvir quando receber o arquivo inteiro
        self.send(server_addr, "PAUSE".encode())

    def listen_file(self, name_file, addr_bind):
        self.storage = []
        self.listen(name_file, addr_bind)

        #remontando o arquivo

    ''' new_file = Path(name_file)
        data = bytearray()
        for i in self.storage:
            data += i

        with new_file.open('wb') as file:
            file.write(data)'''

    def close(self):
        self.sckt.close()
