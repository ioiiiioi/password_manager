import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from dataclasses import dataclass
from typing import Dict

@dataclass
class EncryptedPayload:
    enc_session_key:str
    nonce:str
    ciphertext:str
    tag:str

class RSAEnc:
    """
    Generate key:
        how-to:
            RSAEnc.generate_key()
        return both private and public key in bytes

    Encrypt (DEPRECIATED, ONLY GOOD FOR 190 LONG OF BYTES):
        how-to:
            RSAEnc.encrypt(public_key:str, message:str)
        return ecrypted_message in string

    Decrypt (DEPRECIATED, ONLY GOOD FOR 190 LONG OF BYTES):
        how-to:
            RSAEnc.decrypt(private_key:str, encrypted_msg:str)
        return dict of decrypted messeage

    arbitrary_encrypt:
        Params:
            public_key:str 
            expected as string because usually key will saved ad string 
            instead of PEM file, unless the apps achieving how to save PEM file
            in cloud.

            data:str
            expected data as string, even if data would be dict or list, it needs
            to convert as json first before put in this method.

        Result:
            Dict of "enc_session_key", "nonce", "tag", "ciphertext"
    
    arbitrary_decrypt:
        Params:
            private_key:str 
            expected as string because usually key will saved ad string 
            instead of PEM file, unless the apps achieving how to save PEM file
            in cloud.

            data:dict
            Usually to decrypt some data, it needs "enc_session_key", "nonce", "tag", "ciphertext"
            since the usual RSA encryption only good for 190 bytes. the value of dict
            will be in hex and converted to byte since it came to this method.
            link of reference: https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-rsa

        Result:
        string because it needs to decrypt json form and string form. it will be
        wise if it can maintain as basic form which is string, and form there it
        can converted to either json or just string.

    """

    def generate_key(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.public_key().export_key()
        return private_key, public_key

    def generate_key_as_str(self):
        private, public = self.generate_key()
        private_str = private.decode("utf-8")
        public_str = public.decode("utf-8")
        return private_str, public_str
    
    def load_key(self, key:str):
        bytes_key = key.encode()
        return RSA.import_key(bytes_key)

    def encrypt(self, public_key, message):
        public_key = self.load_key(public_key)
        chiper_rsa = PKCS1_OAEP.new(public_key)
        enc_data = chiper_rsa.encrypt(message)
        enc_data = base64.b64encode(enc_data)
        return enc_data.decode()

    def decrypt(self, private_key, message):
        private_key = self.load_key(private_key)
        message = base64.b64decode(message.encode())
        chiper_rsa = PKCS1_OAEP.new(private_key)
        dec_data = chiper_rsa.decrypt(message)
        data = json.loads(dec_data)
        return data

    def arbitrary_encrypt(self, public_key:str, data:str) -> Dict:
        from Crypto.Random import get_random_bytes

        data = data.encode("utf-8")

        recipient_key = self.load_key(public_key)
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        key = ("enc_session_key", "nonce", "tag", "ciphertext")
        val = (enc_session_key, cipher_aes.nonce, tag, ciphertext)
        result = {value[0]:value[1].hex() for value in list(zip(key, val))}
        return result

    def arbitrary_decrypt(self, private_key:str, data:Dict) -> str:
        data = {key:bytes.fromhex(val) for key, val in data.items()}
        data = EncryptedPayload(**data)

        private_key = self.load_key(private_key)


        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(data.enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, data.nonce)
        result = cipher_aes.decrypt_and_verify(data.ciphertext, data.tag)
        return result.decode("utf-8")