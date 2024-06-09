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

    def close(self):
        self.sckt.close()





