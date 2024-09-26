# mom_encrypter/encrypter.py

import random
import string

def generate_random_string(length=5):
    """Generate a random string of uppercase letters."""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def encrypt(file_name):
    """Encrypt the specified Python file and create a .mom file."""
    try:
        with open(file_name, 'r') as f:
            content = f.read()
        
        mom_file_name = file_name.replace('.py', '.mom')
        with open(mom_file_name, 'w') as f:
            f.write("MOM ENCRYPTED\n")
            f.write("MOM ENCRYPTED\n")
            f.write(generate_random_string() + "\n")  # Add random letters
            f.write(content)  # You can modify this part for actual encryption logic
        
        print(f"{file_name} has been encrypted to {mom_file_name}.")
    except Exception as e:
        print(f"Error encrypting file: {e}")

def unencrypt(mom_file_name):
    """Decrypt the specified .mom file."""
    try:
        original_file_name = mom_file_name.replace('.mom', '.py')
        with open(mom_file_name, 'r') as f:
            lines = f.readlines()
        
        # Skip the first two lines of "MOM ENCRYPTED"
        with open(original_file_name, 'w') as f:
            f.writelines(lines[2:])  # Restore original content
        
        print(f"{mom_file_name} has been unencrypted to {original_file_name}.")
    except Exception as e:
        print(f"Error unencrypting file: {e}")

def run(file_name):
    """Run the encrypted .mom file."""
    try:
        with open(file_name, 'r') as f:
            exec(f.read())  # Be cautious using exec with untrusted code
    except Exception as e:
        print(f"Error running file: {e}")
