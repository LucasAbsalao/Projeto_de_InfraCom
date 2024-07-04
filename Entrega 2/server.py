import Udp
import socket as skt

server = Udp.socketUdp("127.0.0.1", 5555, 1024)
#server.listen_file('received/imageRecebida.jpg')
#server.listen_file('received/textoRecebido.txt')
server.listen_file('received/livroRecebido.pdf')
#server.listen_file('received/musicRecebido.mp3')
