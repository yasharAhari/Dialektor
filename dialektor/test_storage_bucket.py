from django.test import TestCase
from dialektor_files.fileHandling import DialektFileSecurity, StorageBucket
from dialektor.models import metadata
import datetime


class BucketTest(TestCase):

    def setUp(self):
        test_user_name = "Mr. Big Testy"
        self.user_id = DialektFileSecurity.hash_sha256_str(bytes(test_user_name, 'utf-8'))
        metadata.objects.create(user_id=self.user_id,
                                rec_length=datetime.timedelta(minutes=25, seconds=45),
                                fileID="TestFile.file")

        self.file = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque fringilla, quam nec venenatis " \
               b"malesuada, nulla elit aliquam sapien, et maximus ex velit sit amet urna. Integer vitae eros a ex " \
               b"condimentum fermentum sit amet id leo. Cras purus quam, tempor vel nisi ut, ullamcorper luctus quam. " \
               b"Sed in consectetur eros. Etiam tristique orci tortor, eget imperdiet velit molestie ac. Maecenas a " \
               b"diam hendrerit, suscipit lorem id, rhoncus libero. Donec molestie lobortis dolor, non faucibus nisl " \
               b"viverra eu. Vivamus purus lacus, placerat sed mauris ac, pulvinar pellentesque orci. Quisque " \
               b"tincidunt velit sed metus congue aliquet. Nam in mauris purus. Integer eu sollicitudin urna, " \
               b"id venenatis nisl. Quisque facilisis, mi a bibendum lobortis, augue eros faucibus lectus, " \
               b"eget euismod nulla purus nec velit. In ac massa vitae lectus euismod tincidunt eu sed mauris. "

    def test_storage_secure_write_read(self):
        meta_obj = metadata.objects.get(user_id=self.user_id)
        storage_bucket = StorageBucket(meta_obj)
        storage_bucket.file = self.file
        storage_bucket.s_write_file_to_bucket()
        del storage_bucket

        storage_bucket2 = StorageBucket(meta_obj)
        storage_bucket2.s_read_file_from_bucket()
        file_rcv = storage_bucket2.file

        self.assertEqual(self.file, file_rcv, "The file properly saved in Storage")
