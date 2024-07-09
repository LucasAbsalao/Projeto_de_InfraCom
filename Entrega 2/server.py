import Udp
import os
import socket as skt

def check_existing_paths(doc_path):
    if os.path.exists(doc_path):
        os.remove(doc_path)



server = Udp.socketUdp("127.0.0.1", 5555, 1024)
print("Recebendo mensagem do cliente")
check_existing_paths('server_received_docs/image_server.jpg')
server.listen_file('server_received_docs/image_server.jpg')


server = Udp.socketUdp("127.0.0.1", 5555, 1024)
print("Enviando mensagem para o cliente")
addr = ('127.0.0.1', 9999)
server.send_file('server_received_docs/image_server.jpg', addr)

#server.listen_file('server_received_docs/textoRecebido.txt')
#server.listen_file('server_received_docs/livroRecebido.pdf')
#server.listen_file('server_received_docs/musicRecebido.mp3')

