import socket as skt
import time
import os
from client import Client
from server import Server


def check_existing_paths(server_doc_path, client_doc_path):
    if os.path.exists(server_doc_path):
        os.remove(server_doc_path)
    if os.path.exists(client_doc_path):
        os.remove(client_doc_path)


MAX_BUFF_SIZE = 1024
'''teste = [1,2,3]
lista = []
data = bytes(teste)
lista.append(data)
print(lista)

teste = [4,5,6]
data = bytes(teste)
lista.append(data)
print(lista)

arrbyte = bytearray()
for i in lista:
    arrbyte += i
print(arrbyte)'''



addr_bind = ('localhost', 8080)
addr_target = ('localhost', 7070)

server = Server(skt.AF_INET, skt.SOCK_DGRAM, addr_target, MAX_BUFF_SIZE)

client = Client(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)

'''
PARTE 1: ENVIANDO UM ARQUIVO .TXT
'''

name_file = "Assets/song.txt"
server_doc_path = "servidor_docs/arquivo_texto_no_servidor.txt"
client_doc_path = "cliente_docs/arquivo_texto_de_volta_no_cliente.txt"

check_existing_paths(server_doc_path, client_doc_path)


client.send_file(name_file, addr_target)

server.listen_file(server_doc_path,addr_bind)

server.send_file(server_doc_path, addr_bind)

client.listen_file(client_doc_path, addr_target)

'''client.close()
server.close()'''


'''
PARTE 2: ENVIANDO UM ARQUIVO .PNG


server = Server(skt.AF_INET, skt.SOCK_DGRAM, addr_target, MAX_BUFF_SIZE)

client = Client(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
'''

name_file = "Assets/teste2.png"
server_doc_path = "servidor_docs/arquivo_imagem_no_servidor.png"
client_doc_path = "cliente_docs/arquivo_imagem_de_volta_no_cliente.png"

check_existing_paths(server_doc_path, client_doc_path)


client.send_file(name_file, addr_target)

server.listen_file(server_doc_path, addr_bind)

server.send_file(server_doc_path, addr_bind)

client.listen_file(client_doc_path, addr_target)

client.close()
server.close()
