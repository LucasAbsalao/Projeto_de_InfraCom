import socket as skt
import time


class UDP():
    def init(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)

        if self.sckt is None:
            raise "Socket not available."
        
        self.MAX_BUFF = MAX_BUFF

        def listen(self, server_addr: tuple[str, int]):
            while True:
                try:
                    data, origin = self.sckt.recvfrom(self.MAX_BUFF)
                    if str(data)=="STOP":
                        self.send(server_addr, "Saindo".encode())
                        self.sckt.close()
                        break
                except: 
                    continue
        
        def send(self, server_addr: tuple[str, int], msg: bytes):
            #(server_addr = (localhost, port))
            self.sckt.sendto(msg, server_addr)
            time.sleep(0.0001)

MAX_BUFF_SIZE = 1024

addr_bind = ('localhost', 8080)
addr_target = ('localhost', 7070)

client = UDP(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
client.listen()
