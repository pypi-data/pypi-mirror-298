# mom_encrypter/__init__.py

from .encrypter import encrypt, unencrypt, run

class MomwhyareyouhereEncrypter:
    @staticmethod
    def encrypt(filename):
        with open(filename, 'r') as f:
            content = f.read()

        # Simple example of "encryption" by appending 'MOM ENCRYPTED' repeatedly
        encrypted_content = 'MOM ENCRYPTED ' * 10 + ''.join([chr(ord(c) + 1) for c in content])

        # Write to .mom file
        new_filename = filename.replace(".py", ".mom")
        with open(new_filename, 'w') as f:
            f.write(encrypted_content)
        print(f"Encrypted content written to {new_filename}")

    @staticmethod
    def unencrypt(filename):
        with open(filename, 'r') as f:
            content = f.read()

        # Remove the 'MOM ENCRYPTED' text
        if 'MOM ENCRYPTED ' * 10 in content:
            # Simple "decryption" logic: reversing the shift and removing the prefix
            content_without_prefix = content.replace('MOM ENCRYPTED ' * 10, '')
            decrypted_content = ''.join([chr(ord(c) - 1) for c in content_without_prefix])

            # Write to a new .py file
            new_filename = filename.replace(".mom", ".py")
            with open(new_filename, 'w') as f:
                f.write(decrypted_content)
            print(f"Decrypted content written to {new_filename}")
        else:
            print("The file does not appear to be encrypted.")

    @staticmethod
    def run(filename):
        print(f"Running encrypted file: {filename}")
        # You can add custom logic to run the encrypted file if needed
