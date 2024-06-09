import socket as skt
import math

from client import Client
from server import Server

MAX_BUFF_SIZE = 1024

addr_bind = ('localhost', 8080)
addr_target = ('localhost', 7070)

server = Server(skt.AF_INET, skt.SOCK_DGRAM, addr_target, MAX_BUFF_SIZE)

client = Client(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)

'''
PARTE 1: ENVIANDO UM ARQUIVO .TXT
'''

f = open("song.txt", "r")
lyrics = f.read()
lyrics_b = lyrics.encode()

packets = []
j = k = 0
packets.append(bytearray())

# Quebrando o .txt em pacotes de 1024 Bytes

for i in lyrics_b:
    if j < MAX_BUFF_SIZE:
        packets[k].append(i)
        j += 1
    else:
        j = 0
        k += 1
        packets.append(bytearray())

#Enviando cada um dos pacotes
for i in packets:
    client.send(addr_target, i)

#Enviando um sinal de pausa para o server para de ouvir quando receber o arquivo inteiro
client.send(addr_target, "PAUSE".encode())

#Server recebe os pacotes e envia de volta para o cliente
server.listen(addr_target)
for i in server.storage:
    server.send(addr_bind, i)
server.send(addr_bind, "PAUSE".encode())

#Cliente recebe os pacotes de volta
client.listen(addr_bind)

client.close()
server.close()



