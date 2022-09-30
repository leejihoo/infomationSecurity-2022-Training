from socket import AddressFamily, SocketKind, socket
from threading import Thread

# for AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

ENCRYPTION_KEY:bytes = b''
BLOCK_SIZE = 16

text= pad(b'This is a plaintext', BLOCK_SIZE)
#key= b'16byte-key-here!'
key = get_random_bytes(16)
cipher= AES.new(key, AES.MODE_ECB)

class Receiver(Thread):
    def __init__(self, socket:socket):
        super().__init__()
        self.socket = socket

    def decrypt(self, ciphertext:bytes) -> bytes:
        # place your own implementation of
        # AES-128-ECB decryption with pycryptodome
        
        ciphertext= cipher.encrypt(text) # 암호화된결과
        plaintext= cipher.decrypt(ciphertext)
        print( unpad(plaintext, BLOCK_SIZE) ) # This is a plaintext

        return b''

    def handle_recv(self, received:bytes):
        try:
            decrypt_result = self.decrypt(received)
            print("Received: " + bytes.decode(decrypt_result, "UTF-8"))
        except:
            pass

    def run(self):
        while True:
            received:bytes = self.socket.recv(1024)
            self.handle_recv(received)

def encrypt_message(msg: bytes) -> bytes:
    # place your own implementation of
    # AES-128-ECB encryption with pycryptodome

    ciphertext= cipher.encrypt(text)
    print(ciphertext)
    
    return b''

client_socket = socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 24000))

print("[*] connected to 127.0.0.1:24000, Receiving an encryption key...")

# try to receive encryption key (128bits)
ENCRYPTION_KEY = client_socket.recv(16)
print("[*] Key received: " + str(ENCRYPTION_KEY))
print("[*] Now a chatting session is starting...")

# start receiving messages and chatting
Receiver(client_socket).start()

while True:
    msg = input("Message: ")
    msg_encoded = msg.encode("UTF-8")

    payload = encrypt_message(msg_encoded)
    client_socket.send(payload)
    
    print("Me: " + msg)
