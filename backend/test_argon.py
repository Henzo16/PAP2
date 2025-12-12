from argon2 import PasswordHasher

hashed = "$argon2id$v=19$m=65536,t=3,p=4$ASDE+F8rZewdw/h/7z2n9A$kUE9cZzc6ec5ueqwxAmJ/kEJF+CBbo6C+G5GT3ju2BY"

ph = PasswordHasher()

try:
    print(ph.verify(hashed, "123456"))
except Exception as e:
    print("Erro:", e)
