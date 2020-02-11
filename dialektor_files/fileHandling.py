from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
import hashlib
from dialektor.models import metadata
from django.core.files.storage import default_storage

class DialektFileSecurity:
    """
    Dialektor File encryption

    Encrypts and decrypts the data.
    To be used only in with as form

    """
    class FileEncryptUtility:

        def __init__(self, password):
            self.__password = password
            self.__cipher = None
            self.encrypted_data = None
            self.file = None

        def __update_cipher__(self, nonce=None):
            # It is a good security measure to create a new AES object if we are using the same instance to
            # do both operation (rare)
            if self.__cipher is not None:
                del self.__cipher
            if nonce is not None:
                self.__cipher = AES.new(key=self.__password, mode=AES.MODE_EAX, nonce=nonce)
            else:
                self.__cipher = AES.new(key=self.__password, mode=AES.MODE_EAX)

        def __delete__(self, instance):
            del self.__cipher
            del self.__password
            del self.encrypted_data
            del self.file

        def encrypt_file(self):
            """
            Encrypts the file, granted there is a file provided
            grab the result form .encrypted_data
            :return: None
            """
            if self.file is None:
                raise ValueError("No data provided. Please put the data in .file")

            # Update the cipher
            self.__update_cipher__()

            # encrypt the data, collect tag and encrypted data
            cipher_data, tag = self.__cipher.encrypt_and_digest(self.file)

            # collect the nonce
            nonce = self.__cipher.nonce

            # add tag, nonce and encrypted data as one binary data
            self.encrypted_data = tag + nonce + cipher_data
            del self.file
            self.file = None

        def decrypt_file(self):
            """
            Decrypts the file that encrypted with Dialektor cipher
            grab the result from .file
            :return: None
            """
            if self.encrypted_data is None:
                raise ValueError("Data is not provided. Put your data to be encrypted in .encrypted_data")
            try:
                # digest the input file,
                # byte 0-16 tag
                tag = self.encrypted_data[0:16]

                # byte 16-32 nonce
                nonce = self.encrypted_data[16:32]

                # byte 32 - end the encrypted data
                cipher_text = self.encrypted_data[32::]

                # Update the cipher with nonce
                self.__update_cipher__(nonce=nonce)

                # decrypt the data
                self.file = self.__cipher.decrypt_and_verify(ciphertext=cipher_text, received_mac_tag=tag)
                del self.encrypted_data
                self.encrypted_data = None
            except ValueError or KeyError:
                raise ValueError('File Failed to decrypted')

    def __init__(self, password):
        self.password = password
        self.cipher = self.FileEncryptUtility(password=self.password)

    def __enter__(self):
        return self.cipher

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def __delete__(self, instance):
        del self.password
        del self.cipher

    @staticmethod
    def hash_sha256(input_binary):
        """
        Calculates the SHA256 of the input
        :param input_binary: The data to be hashed
        :return: calculated hash of the data in bytes
        """
        hash_f = SHA256.new()
        hash_f.update(input_binary)
        return hash_f.digest()

    @staticmethod
    def hash_sha256_str(input_binary):
        """
        Calculates a sha256 hash of the input and returns an string
        :param input_binary: the data to be hashed
        :return: hash string
        """
        hash_item = hashlib.sha3_256(input_binary)
        return str(hash_item.hexdigest())


class StorageBucket:
    """
    Storage bucket deals with reading and writing Dialektor files to and form storage
    """
    def __init__(self, meta_data: metadata, file=None):
        self.__metadata = meta_data
        self.file_id = self.__metadata.fileID
        self.file_password = DialektFileSecurity.hash_sha256(bytes(self.__metadata.user_id +
                                                                   str(self.__metadata.rec_length) +
                                                                   str(self.__metadata.date_created), 'utf-8'))
        self.file = file

    def s_write_file_to_bucket(self):
        if self.file is None:
            raise ValueError("No File specified")
        with DialektFileSecurity(self.file_password) as cipher:
            cipher.file = self.file
            cipher.encrypt_file()
            file_writer = default_storage.open(self.file_id, 'w')
            file_writer.write(cipher.encrypted_data)
            file_writer.close()

    def s_read_file_from_bucket(self):
        with DialektFileSecurity(self.file_password) as cipher:
            file_reader = default_storage.open(self.file_id, 'r')
            encrypted_file = file_reader.read()
            file_reader.close()
            cipher.encrypted_data = encrypted_file
            cipher.decrypt_file()
            self.file = cipher.file

    def delete_file(self):
        default_storage.delete(self.file_id)

    @staticmethod
    def write_file_to_storage(name, file):
        file_writer = default_storage.open(name, 'w')
        file_writer.write(file)
        file_writer.close()

    @staticmethod
    def read_file_from_storage(name):
        file_reader = default_storage.open(name, 'r')
        file = file_reader.read()
        file_reader.close()
        return file

    @staticmethod
    def delete_given_file(name):
        default_storage.delete(name)
