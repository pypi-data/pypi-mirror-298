import base64
import os
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ..random import rand_letter


def bytes_to_url64str(bstr: bytes):
    s = base64.urlsafe_b64encode(bstr).rstrip(b"=").decode()
    return s


def url64str_to_bytes(s):
    _, r = divmod(len(s), 4)
    bstr = base64.urlsafe_b64decode((s + "=" * r).encode())
    return bstr


def get_key(password, safe_salt=None, times=None):
    if isinstance(password, str):
        password = password.encode()
    if safe_salt is None:
        salt = os.urandom(16)
        safe_salt = bytes_to_url64str(salt)
    else:
        salt = url64str_to_bytes(safe_salt)
    if times is None:
        times = random.randint(100, 100000)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=times,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return (key, safe_salt, times)


def str_randsplit_to_list(s, n1=10, n2=30):
    r = []
    while s:
        if len(s) < 40:
            r.append(s)
            break
        k = random.randint(n1, n2)
        r.append(s[:k])
        if k < len(s):
            s = s[k:]
        else:
            s = ""
    return r


def encrypt_str_to_list(s: str, password=None, prefix=None):
    if password is None:
        password = rand_letter(random.randint(6, 16))
        out_password = password
    else:
        out_password = "-"
    if prefix is not None:
        password = str(prefix) + password

    key, safe_salt, times = get_key(password)

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(s.encode())
    safe_data = bytes_to_url64str(encrypted_data)

    list_out = [out_password, safe_salt, str(times)] + str_randsplit_to_list(safe_data)

    return list_out


def decrypt_list_to_str(list_in, password=None, prefix=None):
    _password, safe_salt, _times, *_data = list_in
    if password is None:
        password = _password
    else:
        password = password
    if prefix is not None:
        password = str(prefix) + password

    times = int(_times)
    s = "".join(_data)
    key, _, _ = get_key(password, safe_salt, times)
    cipher_suite = Fernet(key)
    decrypted_bytes = cipher_suite.decrypt(url64str_to_bytes(s))
    return decrypted_bytes.decode()
