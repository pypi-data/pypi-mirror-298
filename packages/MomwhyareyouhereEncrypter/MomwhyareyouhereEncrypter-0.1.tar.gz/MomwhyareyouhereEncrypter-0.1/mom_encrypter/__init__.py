# mom_encrypter/__init__.py

from .encrypter import create_mom_file, run_mom_file

class MomwhyareyouhereEncrypter:
    @staticmethod
    def create(file_name):
        create_mom_file(file_name)

    @staticmethod
    def run(file_name):
        run_mom_file(file_name)
