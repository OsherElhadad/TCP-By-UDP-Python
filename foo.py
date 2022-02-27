from socket import socket,AF_INET,SOCK_DGRAM
import sys, random, traceback
from datetime import datetime
from threading import Thread
from time import sleep

MY_PORT = int(sys.argv[1])
ALICE_IP = sys.argv[2]
ALICE_PORT = int(sys.argv[3])
ALICE_ADDR = (ALICE_IP, ALICE_PORT)
MODE = int(sys.argv[4])


s = socket(AF_INET,SOCK_DGRAM)
s.bind(('', MY_PORT))

def send(data, addr):
    if addr != ALICE_ADDR:
        s.sendto(data, ALICE_ADDR)
        print(f'Forwarded {data} from {addr} to {ALICE_ADDR}')
    else:
        s.sendto(data, BOB_ADDR)
        print(f'Forwarded {data} from {addr} to {BOB_ADDR}')

def delayed(data, addr):
    delay = random.randrange(5000) / 1000
    print(f'Delaying! for {delay} seconds...')
    sleep(delay)
    send(data, addr)

x = datetime.now()

random.seed(int(x.strftime("%f")))

DROP_RATE = 100
DELAY_RATE = 100

if MODE == 1:
    print('Playing nice')

if (MODE == 2) or (MODE == 4):
    DROP_RATE = random.randrange(99)
    print(f'Dropping {100-DROP_RATE}%')
    
if (MODE == 3) or (MODE == 4):
    DELAY_RATE = random.randrange(100)
    print(f'Delaying {100-DELAY_RATE}%')


data, BOB_ADDR = s.recvfrom(101)
addr = BOB_ADDR

while True:
    try:
        drop = random.randrange(100)
        if (len(data) <= 100) and (drop < DROP_RATE):

            print(f'Phiiiii, no drop.... {drop}')

            delay = random.randrange(100)
            if (delay > DELAY_RATE):
                print(f'Good night.... {delay} {DELAY_RATE}')                
                t = Thread(target = delayed, args = (data, addr, ))
                t.start()
            else:
                print(f'Yay, no sleep.... {delay} {DELAY_RATE}')
                send(data, addr)

        else:
            if len(data) > 100:
                print('Dropped! too big...')
            else:
                print('Dropped! randomly... ', str(drop))

    except Exception:
        traceback.print_exc()
        
    finally:
        data, addr = s.recvfrom(100)        
