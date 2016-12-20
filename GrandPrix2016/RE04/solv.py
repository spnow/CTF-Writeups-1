key1 = "#$A^I&*R"
key2 = "01633"
flag = ""
res = open("abc.txt","rb").read()
enc1 = res[2056:2056 + 0x18].replace("[","=").decode("base64").replace("\x00", "")
enc2 = res[4162:4162 + 0x19].replace("[","=").decode("base64").replace("\x00", "")
enc3 = res[5129:5129 + 0x0c].replace("[","=").decode("base64").replace("\x00", "")
enc4 = res[5141:5141 + 0x05]

for i in range(len(enc1)):
	flag += chr(ord(enc1[i]) ^ ord(key1[i % len(key1)]))

flag += "_"
flag += enc2 + enc3

for i in range(len(enc4)):
	flag += chr(ord(enc4[i]) ^ ord(key2[i % len(key2)]))

print flag
#Whjt3_H4t_C0nt3st S0 Funnij

