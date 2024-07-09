import Udp
import socket as skt

addr = ('127.0.0.1',5555)

client = Udp.socketUdp("127.0.0.1", 9999, 1024)
print("Enviando mensagem para o servidor")
client.send_file('files/image.jpg', addr)

client = Udp.socketUdp("127.0.0.1", 9999, 1024)
print("Recebendo mensagem do servidor")
client.listen_file('client_received_docs/image_client.jpg')

#client.send_file('files/texto.txt', addr)
#client.send_file('files/livro.pdf', addr)
#client.send_file('files/music.mp3', addr)
