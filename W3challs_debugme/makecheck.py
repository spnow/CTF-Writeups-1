import os
os.system("nasm -fbin check.asm")

asm = open("check","rb").read()
asm = "".join(["\\x%02x"%ord(i) for i in asm])

fic = open("check.c","w")
print >>fic, """#include "check.h"\n\rchar *check = """,
for i in range(0,len(asm),80):
	print >>fic, '"%s"' % asm[i:i+80]
print >>fic, ";"
