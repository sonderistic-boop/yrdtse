import socket
import pickle


class Network:
    def __init__(self,serverIp,port,initialData):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIp = serverIp
        self.port = 5555
        self.address = (self.serverIp, self.port)
        self.initialData = self.initialConnect(initialData)
        print(self.initialData)

    def getInitData(self):
        return self.initialData

    def initialConnect(self,data):
        try:
            
            self.client.connect(self.address)
            self.client.send(pickle.dumps(data))
            
            return pickle.loads(self.client.recv(4096))
        except:
            pass

    def sendData(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
    def close(self):
        self.client.close()




def get_ip():
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSocket.settimeout(0)
        try:
            #connect to dummy server to get ip
            tempSocket.connect(('8.8.8.8', 1))
            ip = tempSocket.getsockname()[0]
        except Exception:
            #if connection fails, most likely because linux shenanigans, use 127.0.0.1
            ip = '127.0.0.1'
        finally:
            tempSocket.close()
        return ip
    