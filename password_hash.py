import hashlib

password1 = "password123"
password2 = "bhaskar123"

hashed_password1 = hashlib.md5(password1.encode()).hexdigest()
hashed_password2 = hashlib.md5(password2.encode()).hexdigest()

print(hashed_password1)
print(hashed_password2)