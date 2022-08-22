import binascii

mes = "123asd"
hmes = binascii.hexlify(mes.encode("ascii"))

print(mes)
print(hmes)


