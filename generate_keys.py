# generate_keys.py - Run this FIRST to create your RSA keys
from Cryptodome.PublicKey import RSA

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    with open("private_key.pem", "wb") as priv_file:
        priv_file.write(private_key)
    
    with open("public_key.pem", "wb") as pub_file:
        pub_file.write(public_key)
    
    print("Keys generated successfully!")
    print("\nPublic Key (paste this into lab.py):")
    print(public_key.decode())

if __name__ == "__main__":
    generate_key_pair()