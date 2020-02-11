from django.test import TestCase
from dialektor_files.fileHandling import DialektFileSecurity

class EncryptionTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_file_encryption_decryption(self):
        print("Testing encryption...")
        file = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque fringilla, quam nec venenatis " \
               b"malesuada, nulla elit aliquam sapien, et maximus ex velit sit amet urna. Integer vitae eros a ex " \
               b"condimentum fermentum sit amet id leo. Cras purus quam, tempor vel nisi ut, ullamcorper luctus quam. " \
               b"Sed in consectetur eros. Etiam tristique orci tortor, eget imperdiet velit molestie ac. Maecenas a " \
               b"diam hendrerit, suscipit lorem id, rhoncus libero. Donec molestie lobortis dolor, non faucibus nisl " \
               b"viverra eu. Vivamus purus lacus, placerat sed mauris ac, pulvinar pellentesque orci. Quisque " \
               b"tincidunt velit sed metus congue aliquet. Nam in mauris purus. Integer eu sollicitudin urna, " \
               b"id venenatis nisl. Quisque facilisis, mi a bibendum lobortis, augue eros faucibus lectus, " \
               b"eget euismod nulla purus nec velit. In ac massa vitae lectus euismod tincidunt eu sed mauris. "
        password = DialektFileSecurity.hash_sha256(b"MyPassWord?")
        encrypted_data = None
        decrypted_file = None
        with DialektFileSecurity(password) as cipher:
            cipher.file = file
            cipher.encrypt_file()
            encrypted_data = cipher.encrypted_data

        with DialektFileSecurity(password) as cipher2:
            cipher2.encrypted_data = encrypted_data
            cipher2.decrypt_file()
            decrypted_file = cipher2.file
        self.assertEqual(file, decrypted_file)

