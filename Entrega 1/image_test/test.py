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
PARTE 1: ENVIANDO UMA IMAGEM
'''
name_file = "imagem.jpg"

client.send_file(name_file, addr_target)

server.listen_file("arquivo_no_servidor.txt",addr_bind)

server.send_file("arquivo_no_servidor.txt", addr_bind)

client.listen_file("arquivo_de_volta_no_cliente.txt", addr_target)

client.close()
server.close()



