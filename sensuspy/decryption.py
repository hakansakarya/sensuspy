import os
import glob
import struct
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

#Decrypts Sensus .bin files that were encrypted using asymmetric encryption
def decrypt_bin_files(data_path, rsa_private_key_path, is_directory = True, recursive = True, replace_files = True, rsa_private_key_password = None):

    if is_directory:
        if recursive:
            bin_paths = glob.glob(data_path + '*/**/*.bin', recursive=True)
        else:
            bin_paths = glob.glob(os.path.join(data_path,'*.bin'))

        if len(bin_paths) == 0:
            print("Could not find any bin files to decrypt.")
            return None

    else:
        bin_paths = data_path
        path_check = paths.split(".")
        file_extension = path_check[len(path_check)-1]

        if not file_extension == "bin":
            print("Path is not a bin file.")
            return None

    if not os.path.exists(rsa_private_key_path):
        print("RSA private key path does not exist.")
        return None
        
    else:
    
        rsa_cipher = load_rsa_key(rsa_private_key_path,rsa_private_key_password)

        print("Decrypting " + str(len(bin_paths)) + " file(s)...")

        file_number = 0

        #enc_tuples = []
        index = 0
        for bin_path in bin_paths:

            file_number += 1
            print("Decrypting file " + str(file_number) + " of " + str(len(bin_paths)))

            try:
                with open(bin_path, 'rb') as bin_file: 
                    enc_aes_key_size = struct.unpack('<I', bin_file.read(4))[0]
                    enc_aes_key = bin_file.read(enc_aes_key_size)
                    
                    enc_aes_iv_size = struct.unpack('<I', bin_file.read(4))[0]
                    enc_aes_iv = bin_file.read(enc_aes_iv_size)
                    
                    file_size_bytes = os.path.getsize(bin_path)
                    data_size_bytes = file_size_bytes - (4 + enc_aes_key_size + 4 + enc_aes_iv_size)
                    
                    enc_data = bin_file.read(data_size_bytes)
                    empty_check = bin_file.read()

                if not len(empty_check) == 0:
                    print("Decryption error:  Leftover bytes in data segment. Proceeding with decryption anyway, but there is something seriously wrong.")

                aes_key = rsa_cipher.decrypt(enc_aes_key,padding.PKCS1v15())
                aes_iv = rsa_cipher.decrypt(enc_aes_iv,padding.PKCS1v15())
                
                aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
                aes_decryptor = aes_cipher.decryptor()
                data = aes_decryptor.update(enc_data) + aes_decryptor.finalize() 

                #remove padding
                padding_bytes = data[-1]
                data = data[:-padding_bytes]

                #remove .bin extension
                decrypted_path = bin_path.rsplit(".",1)[0]
                with open(decrypted_path, 'wb') as dec_file:
                    dec_file.write(data)

                index += 1
                
            except Exception as Error:
                print(Error)

        if replace_files:
            for bin_path in bin_paths:
                try:
                    os.remove(bin_path)
                except Exception as Error:
                    print(Error)


def load_rsa_key(rsa_key_path, rsa_key_password=None):

    if rsa_key_password == None:
        rsa_key_password = input("Enter rsa key password: ")

    with open(rsa_key_path,'rb') as keyfile:
        pk = serialization.load_pem_private_key(keyfile.read(),password=rsa_key_password.encode('utf-8'),backend=default_backend())

    return pk


