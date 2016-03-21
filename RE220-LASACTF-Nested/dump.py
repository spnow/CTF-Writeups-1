from struct import unpack,pack
from capstone import *
def unNest(input,output):
    f = open(input,"rb")
    f.seek(0x200)
    raw = f.read(0xff)
    CODE = raw[raw.index("\x8a\x01")+2:raw.index("\x88\x01")]
    a =  raw.index("\xc3\x68")

    f.seek(0x200+a+2)
    size = f.read(3) + "\x00" 
    size = (unpack("<I", size)[0])
    f.seek(0x400)
    a =  f.read(100).index("\x0a")
    f.seek(0x400+a+2)

    Data = f.read(size)
    f.close()
    def fix(byte):
        if byte[:2] == "0x":
            byte = byte[2:]
        return byte.strip()
        
    md = Cs(CS_ARCH_X86, CS_MODE_64).disasm(CODE,0x1000)
    vlist = []
    mlist = []
    for i in md:
        val =  int(fix(i.op_str[5:]),16)
        vlist.append(val)
        mlist.append(i.mnemonic)
        
    def calc(byte):
        byte = ord(byte)
        for i in range(len(vlist)):
            val =  vlist[i]
            b = mlist[i]
            if b == "add":
                byte = (byte + val) & 0xff
            elif b == "sub":
                byte = (byte - val) & 0xff
            elif b == "xor":
                byte = (byte ^ val) & 0xff
                
        return chr(byte)

    w = open(output,"wb")
    for i in Data:    
        w.write(calc(i))
    w.close()

input = "solve_me.exe"
for i in range(0xff):
    print i
    unNest(input,str(i))
    input = str(i)
    