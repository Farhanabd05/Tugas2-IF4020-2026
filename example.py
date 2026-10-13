from src import encrypt, decrypt

key = "KeyYoisakiKanade"
iv  = b"FEDCBA9876543210"
counter = b"FAFAFAFAFAFAFAFA"

plaintext = "I imagine death so much it feels more like a memory. When is it going to get me? In my sleep? Seven feet ahead of me? If I see it coming, do I run or do I let it be? Is it like a beat without a melody? See, I never thought I would live past twenty. Where I come from some get half as many. Ask anybody why we living fast and we laugh, reach for a flask. We have to make this moment last, that is plenty. Scratch that. This is not a moment, it is the movement. Where all the hungriest brothers with something to prove went? Foes oppose us, we take an honest stand. We roll like Moses, claiming our promised land. And? If we win our independence? Is that a guarantee of freedom for our descendants? Or will the blood we shed begin an endless cycle of vengeance and death with no defendants? I know the action in the street is exciting. But Jesus, between all the bleeding and fighting. I have been reading and writing. We need to handle our financial situation. Are we a nation of states? What is the state of our nation? I am past patiently waiting. I am passionately smashing every expectation. Every action is an act of creation! I am laughing in the face of casualties and sorrow. For the first time, I am thinking past tomorrow!"

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