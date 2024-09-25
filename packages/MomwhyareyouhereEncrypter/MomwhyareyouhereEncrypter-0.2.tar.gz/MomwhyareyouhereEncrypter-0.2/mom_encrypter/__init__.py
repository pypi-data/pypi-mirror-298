# mom_encrypter/__init__.py

from .encrypter import encrypt, unencrypt, run

class MomwhyareyouhereEncrypter:
    @staticmethod
    def encrypt(file_name):
        encrypt(file_name)

    @staticmethod
    def unencrypt(mom_file_name):
        unencrypt(mom_file_name)

    @staticmethod
    def run(file_name):
        run(file_name)
