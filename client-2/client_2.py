import socket
import multiprocessing
import json


class Writer:
    def __init__(self):
        self.datas = multiprocessing.Queue()

    def start(self,file_name):
        self.process = multiprocessing.Process(target=self.writeLoop,args=[file_name])
        self.process.start()

    def write(self,data):
        self.datas.put(data)

    def writeLoop(self,file_name):
        print('open',file_name)
        fd = open(file_name,'wb+',0)
        while True:
            while not self.datas.empty():
                fd.write(self.datas.get())

    def stop(self):
        self.process.terminate()



CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 9002
CLIENT = (CLIENT_IP,CLIENT_PORT)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000
SERVER = (SERVER_IP,SERVER_PORT)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(CLIENT)

while True:
    request = "init_connection"

    print('Send register request to server')
    sock.sendto(bytes(request),SERVER)
    data, server_address = sock.recvfrom(1024)
    if data.decode('utf-8') == 'accepted':
        print('Registered to the server')
        ditulis = 0
        while True:
            ditulis += 1
            data, addr = sock.recvfrom(1024)
            json_acceptable_string = data.replace("'", "\"")
            header = json.loads(json_acceptable_string)
            sock.settimeout(0.1)
            fd = open(header['file_name'], 'wb+', 0)
            try:
                counter = 0
                while True:
                    data, addr = sock.recvfrom(2048)
                    counter += 1
                    print('blok {}'.format(counter), len(data))
                    fd.write(data)
            except:
                not_complete = False
                fd.close()
                sock.settimeout(10000)