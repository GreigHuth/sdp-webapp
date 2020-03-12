

import socket

import pickle

labels = ['DG311 Gib.', 'BJ1499.S5 Kag.', 'QC21.3 Hal.', 'QC174.12 Bra.', 'PS3562.E353 Lee.',

          'PR4662 Eli.', 'HA29 Huf.', 'QA276 Whe.', 'QA76.73.H37 Lip.', 'QA76.62 Bir.']

target_label = ['DG311 Gib.']

HOST = 'middleton'

PORT = 50000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    xs = [1,2,3,4]

    s.sendall(pickle.dumps((target_label, labels)))

    data = s.recv(1024)

print('Received: ', pickle.loads(data))


