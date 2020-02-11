
from fileHandling import DialektFileSecurity


def test_file_encryption():
    print("Starting test")
    my_file_raw = b"Hello There, stuff stuff stuff stuff ... bla bla bla..."
    with DialektFileSecurity(DialektFileSecurity.hash_sha256(b'my password')) as dfs:
        dfs.file = my_file_raw
        dfs.encrypt_file()
        print(dfs.encrypted_data)
        print("Encryption Done")
        dfs.decrypt_file()
        print(dfs.file)
        if dfs.file == my_file_raw:
            print("test pass")


test_file_encryption()
