__author__ = "Sait Hakan Sakarya"
__email__ = "shs5fh@virginia.edu"

import os
import glob
import gzip
import struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5


def sync_from_aws(s3_path, local_path, profile = "default", aws_client_path = "/usr/local/bin/aws", delete = False, decompress_files = True):
    """Synchronizes data from Amazon S3 to a local path using the AWS client - AWS client needs to be installed"""

    aws_args = "s3 --profile " + profile + " sync " + s3_path + " " + local_path

    if delete:
        aws_args += " --delete"

    if os.name == "posix":
            aws_client_path = os.popen('which aws').read().strip()

    invoke_command = aws_client_path + " " + aws_args

    try:
        os.system(invoke_command)
        if decompress_files:
            decompress(local_path)

    except Exception as e:
        print(e)
        
       
def decompress(local_path):
    """Decompresses .gz files downloaded from Amazon S3"""
    
    paths = glob.glob(data_path + '*/**/*.gz', recursive=True)
    
    if len(paths) == 0:
        print("No files no decompress.")

    else:

        print("Decompressing " + str(len(paths)) + " files.")

        for path in paths:
            try:
                decompressed_name = path[:-3]
                with gzip.open(path, 'rb') as infile, open(decompressed_name, 'wb') as outfile:
                    content = infile.read()
                    outfile.write(content)
                os.remove(path)

            except Exception as Error:
                print(Error)

