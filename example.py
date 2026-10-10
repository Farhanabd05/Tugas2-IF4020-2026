from src import encrypt, decrypt

key = "KeyYoisakiKanade"
iv  = b"FEDCBA9876543210"
counter = b"FAFAFAFAFAFAFAFA"

plaintext = "It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

print("cbc")
ciphertext = encrypt(plaintext, key, "cbc", iv=iv)
print(ciphertext.hex())
decrypted = decrypt(ciphertext, key, "cbc", iv=iv)
print(decrypted)

print()

print("cfb")
ciphertext = encrypt(plaintext, key, "cfb", iv=iv)
print(ciphertext.hex())
decrypted = decrypt(ciphertext, key, "cfb", iv=iv)
print(decrypted)

print()

print("ctr")
ciphertext = encrypt(plaintext, key, "ctr", counter=counter)
print(ciphertext.hex())
decrypted = decrypt(ciphertext, key, "ctr", counter=counter)
print(decrypted)

print()

print("ecb")
ciphertext = encrypt(plaintext, key, "ecb")
print(ciphertext.hex())
decrypted = decrypt(ciphertext, key, "ecb")
print(decrypted)

print()

print("ofb")
ciphertext = encrypt(plaintext, key, "ofb", iv=iv)
print(ciphertext.hex())
decrypted = decrypt(ciphertext, key, "ofb", iv=iv)
print(decrypted)