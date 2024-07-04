import Udp
import socket as skt

addr = ('127.0.0.1',5555)

client = Udp.socketUdp("127.0.0.1", 9999, 1024)
#client.send_file('files/image.jpg', addr)
#client.send_file('files/texto.txt', addr)
client.send_file('files/livro.pdf', addr)
#client.send_file('files/music.mp3', addr)
