
# Copyright (c) 2025 JavaPythonLua
# Licensed under the GNU General Public License - See LICENSE file for details.

import socket
import multiprocessing
import time
import queue
import threading
import json
import os
import shutil
import logging
ans_queue = queue.Queue()
addr_queue = queue.Queue()
conn_queue = queue.Queue()
nickname_queue = queue.Queue()
addr_list = []
conn_list = []
def accept_conn(s,addr_queue,conn_queue,nickname_queue):
    while conns == True:
        conn,addr = s.accept()
        print(f"got connection from {str(addr)}")
        conn_queue.put(conn)
        addr_queue.put(addr)
        nickname = conn.recv(1024).decode('utf-8')
        nickname_queue.put(nickname)
        print(f'"{nickname}" joined the game')
def wait_for_start():
    global conns
    input("Press enter to start...")
    conns = False
def handle_qs(s,conn,ans_queue):
    logging.debug("handle_qs")
    conn.send("Q".encode('utf-8'))
    logging.debug("Message sent")
    message = conn.recv(1024).decode('utf-8')
    ans = (conn,message)
    ans_queue.put(ans)


kpack = input("What is the pack name?")
kpackx = kpack + ".kpack"
tarpack = kpack + ".tar"
os.rename(kpackx,tarpack)
os.makedirs(kpack)
shutil.unpack_archive(tarpack,kpack,'tar')
os.rename(tarpack,kpackx)
metafile = open(kpack+"/"+"pack.khmeta")
meta = json.load(metafile)
metafile.close()
QuizName = meta["Name"]
questions_file = kpack+"/assets/"+QuizName+"/questions.json"
qsf = open(questions_file,'r')
qs = json.load(qsf)
qsf.close()





connstup = tuple() 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
OPORT = 0
s.bind((HOST,OPORT))
PORT = s.getsockname()
SOCK_LIST = list(str(PORT))
for i in range(0,17):
    SOCK_LIST[i] = ""
SOCK_LIST[-1] = ""
PORT = ''.join(SOCK_LIST)
print(f"The host is: {HOST}")
print(f"The port is: {PORT}")
s.listen()
global conns
conns = True
conns_queue = threading.Thread(target=accept_conn,args=(s,addr_queue,conn_queue,nickname_queue))
conns_queue.start()
rounds = 0
wait_start_thread = threading.Thread(target=wait_for_start)
wait_start_thread.start()
while conns == True:
    conn = conn_queue.get()
    connstup = connstup + (conn,)
wait_start_thread.join()





noQs = int(meta["nq"])
for f in range(0,noQs):
    index = "Q"+str(f+1)
    correct_ans = qs[index]["correct_answer"]
    print(index+":")
    print(qs[index]["question"])
    print("A: " + qs[index]["answers"][0])
    print("B: " + qs[index]["answers"][1])
    print("C: " + qs[index]["answers"][2])
    logging.debug(len(connstup))
    for i in range(0,len(connstup)):
        logging.debug("Loop1")
        threading.Thread(target=handle_qs,args=(s,connstup[i],ans_queue,)).start()
        logging.debug("Thread")
    while len(connstup) > rounds:
        ans = ans_queue.get()
        if ans[1] == correct_ans:
            ans[2].send("correct".encode('utf-8'))
            rounds += 1
        elif rounds != None:
            ans[2].send("wrong".encode('utf-8'))
            rounds += 1
        else:
            pass
