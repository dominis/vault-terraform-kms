# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import sarge
import base64
from boto import kms
from Crypto.Cipher import AES

def runner(cmd):
    """Shell command runner"""
    try:
        return sarge.run(
            cmd,
            stdout=sarge.Capture(),
            stderr=sarge.Capture()
        )
    except Exception, e:
        raise


pad = lambda s: s + (32 - len(s) % 32) * ' '


def get_arn(aws_data):
    """Generate ARN from aws data"""
    return 'arn:aws:kms:{region}:{account_number}:key/{key_id}'.format(**aws_data)


def kms_encrypt_data(aws_data, plaintext_message):
    """Encrypt plaintext"""
    conn = kms.connect_to_region(aws_data['region'])
    arn = get_arn(aws_data)

    data_key = conn.generate_data_key(arn, key_spec='AES_128')
    ciphertext_blob = data_key.get('CiphertextBlob')
    plaintext_key = data_key.get('Plaintext')

    # Note, does not use IV or specify mode... for demo purposes only.
    crypter = AES.new(plaintext_key)
    encrypted_data = base64.b64encode(crypter.encrypt(pad(plaintext_message)))

    # Need to preserve both of these data elements
    return encrypted_data, ciphertext_blob

def kms_decrypt_data(aws_data, encrypted_data, ciphertext_blob):
    """Decrypt data"""
    conn = kms.connect_to_region(aws_data['region'])

    decrypted_key = conn.decrypt(ciphertext_blob).get('Plaintext')
    crypter = AES.new(decrypted_key)

    return crypter.decrypt(base64.b64decode(encrypted_data)).rstrip()


def vault_init():
    """Initailaize empty vault"""
    vault_init = 'vault init -key-shares=1 -key-threshold=1 | '\
        'head -1 |' \
        'cut -d":" -f 2 |' \
        'xargs'

    res = runner(vault_init)
    if res.returncode:
        print(res.stderr.text)
    else:
        return res.stdout.text.strip()


def vault_unseal(master_key):
    """Unseal running vault"""
    vault_unseal = 'vault unseal {}'.format(master_key)
    res = runner(vault_unseal)
    return res


def main():
    aws_data = {
        'region': 'xxx',
        'account_number': 'xxx',
        'key_id': 'xxx',
    }


    # `vault status` outputs whether or not the Vault is sealed. The exit
    # code also reflects the seal status (0 unsealed, 2 sealed, 1 error).
    res = runner('vault status')
    if res.returncode == 1:
        master_key = vault_init()
        encrypted_data, ciphertext_blob = kms_encrypt_data(aws_data, master_key)
    elif res.returncode == 2:
        master_key = kms_decrypt_data(aws_data, encrypted_data, ciphertext_blob)
        vault_unseal(master_key)
    else:
        print('Vault is initalized and unsealed.')


if __name__ == '__main__':
    main()
