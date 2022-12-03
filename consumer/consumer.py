import socket
import time
import threading
import asyncio
import csv
import util

CONSUMER_PORT = 33533
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class Consumer:
    def __init__(self, host):
        self.host = host

    def listen_device(self):
        key1 = util.load_private_key('./privateKey.pem')
        key2 = util.load_pub_key('./certificate.pem')
        try:
            sock.bind((self.host, CONSUMER_PORT))
            while True:
                msg, addr = sock.recvfrom(1024)
                value1 = util.encrypt_with_rsa(msg.decode('utf-8').split(',')[3].encode(), key2)
                # value2= msg.decode('utf-8').split(',')[3].encode()
                # print(util.decrypt_with_rsa(value1, key1))
                value2 = msg.decode('utf-8').split(',')[3]
                print(value2)
        finally:
            sock.close()
            print('socket close')

    async def send_interest(self):
        isLoop = True;

        async def _(event):
            nonlocal isLoop
            isLoop = False
            event.app.exit()

        while isLoop:
            try:
                with open('./interest.csv', 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        interest_name = row
                        time.sleep(2)
                        msg = bytes('interest,'.encode()) + bytes(str(interest_name[0]).encode()) + bytes(
                            ',consumer'.encode())
                        print(msg)
                        # print(str(line[1]))
                        sock.sendto(msg, ('127.0.0.1', 33343))

            except KeyboardInterrupt:
                return

    async def main(self):
        await self.send_interest()

    def run(self):
        try:
            from asyncio import run
        except ImportError:
            asyncio.run_until_complete(self.main())
        else:
            asyncio.run(self.main())


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    consumer = Consumer(host)
    listen_thread = threading.Thread(target=consumer.listen_device)
    listen_thread.setDaemon(True)
    listen_thread.start()
    consumer.run()
