
from socket import *

from multiprocessing import Process





def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))



def recvMsg():
    pass


def sendMsg(msg):
    pass


if __name__ == "__main__":

    #clientSock = socket(AF_INET, SOCK_STREAM)
    #clientSock.connect(('127.0.0.1', 7889))
    recvProcess = Process(target=recvMsg,args=())
    sendMsgProcess = Process(target=sendMsg,args=())












