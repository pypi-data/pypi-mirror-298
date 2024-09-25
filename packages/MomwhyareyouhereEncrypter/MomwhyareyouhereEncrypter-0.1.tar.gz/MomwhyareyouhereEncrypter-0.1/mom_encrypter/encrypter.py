# mom_encrypter/encrypter.py
import random
import string

def create_mom_file(file_name):
    # Create a .mom file with the specified content
    with open(f"{file_name}.mom", "w") as f:
        f.write("MOM ENCRYPTED\n")
        f.write("MOM ENCRYPTED\n")
        # Spamming random letters
        random_letters = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=100))
        f.write(random_letters)

def run_mom_file(file_name):
    try:
        with open(file_name, "r") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("File not found. Make sure the .mom file exists.")
