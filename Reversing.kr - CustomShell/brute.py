def ror(a,b):
    return ((a>>b) ^ (a<<(8-b)))&0xff

def getrorindex(r24, r22,r9):
    carry = 0
    r25 = r9
    r26 = 0
    r23 = 0
    r27 = 0
    i = 0x11
    while(1):
        r24 = (r24 << 1) + carry
        carry = (r24 & 0x100) >> 8
        r24 &= 0xff
        
        r25 = (r25 << 1) + carry
        carry = (r25 & 0x100) >> 8
        r25 &= 0xff
        i -= 1
        if i == 0:
            break
        r26 = (r26 << 1) + carry
        carry = (r26 & 0x100) >> 8
        r26 &= 0xff


        r27 = (r27 << 1) + carry
        carry = (r27 & 0x100) >> 8
        r27 &= 0xff

        tmp = r26 - r22
        carry = (tmp & 0x100) >> 8
        tmp &= 0xff

        tmp = r27 - r23 - carry
        carry = (tmp & 0x100) >> 8
        tmp &= 0xff
        
        if carry == 0:
            r26 = (r26 - r22) & 0xff
    r24 = (0xff-r24)&0xff
    r25 = (0xff-r25)&0xff
    return (r24,r26)

def brute(dest, pos,sums,r9):
	for ii in range(0xff):
		ip = [ii]*9
		id = [0]*0xfff
		id[0x100] = 0x4a
		id[0x101] = 0x16
		id[0x102] = 0x71
		id[0x103] = 0x2c
		id[0x104] = 0x11
		id[0x105] = 0xbb
		id[0x106] = 0xaf
		id[0x107] = 0x1e
		id[0x108] = 0xb8
		id[0x109] = 0x9f
		id[0x10a] = 0x68
		id[0x10b] = 0xd3
		id[0x10c] = 0x37
		id[0x10d] = 0xcd
		id[0x10e] = 0x55
		id[0x10f] = 0x1b
		id[0x110] = 0xb7
		id[0x111] = 0xa8
		id[0x112] = 0x02
		id[0x113] = 0xbd
		id[0x114] = 0x0b
		id[0x115] = 0xff
		id[0x116] = 0xee
		id[0x117] = 0x8e
		id[0x118] = 0x30
		id[0x119] = 0xc9
		id[0x11a] = 0xd7
		id[0x11b] = 0x12
		id[0x11c] = 0xe8
		id[0x11d] = 0x60
		id[0x11e] = 0x0a
		id[0x11f] = 0x4b
		id[0x120] = 0x01
		id[0x121] = 0x00

		id[0x122] = 0x00
		id[0x123] = 0x00
		id[0x124] = 0x00
		id[0x125] = 0x00
		id[0x126] = 0x14
		id[0x127] = 0x00
		id[0x128] = 0x58
		id[0x129] = 0x05
		id[0x12a] = 0x15
		id[0x12b] = 0x00
		id[0x12c] = 0x66
		id[0x12d] = 0x05
		id[0x12e] = 0x16
		id[0x12f] = 0x00
		id[0x130] = 0x73
		id[0x131] = 0x05
		id[0x132] = 0x1f
		id[0x133] = 0x00
		id[0x134] = 0x82
		id[0x135] = 0x05
		id[0x136] = 0x28
		id[0x137] = 0x00
		id[0x138] = 0x10
		id[0x139] = 0x06
		id[0x13a] = 0x29
		id[0x13b] = 0x00
		id[0x13c] = 0x10
		id[0x13d] = 0x06
		id[0x13e] = 0x2a
		id[0x13f] = 0x00
		id[0x140] = 0x10
		id[0x141] = 0x06



		id[0xae4] = 0x4a
		id[0xae5] = 0x18
		id[0xae6] = 0xaf
		id[0xae7] = 0xf7
		id[0xae8] = 0x81
		id[0xae9] = 0x6a
		id[0xaea] = 0xd7
		id[0xaeb] = 0x3a
		id[0x628] = 3
		id[0x627] = 2
		id[0x624] = 1

		st = 0x100
		st2 = 0
		def getindex(a):
			a = (a - 1) & 0xff
			if a > 5:
				return 0
			a = (a - 0xdc) & 0xff
			a = 0x600 ^ a
			#print ">>>>", hex(a)
			return id[a]
			
		def getindex2(a):
			if a == 4 or a == 2 or a == 8:
				return 1
			if a == 0x10 or a == 0x20 or a == 0x80 or a == 0x40:
				return 2
			if a == 0x24 or a == 0x42 or a== 0x81 or a== 0x18:
				return 3
			return 0

		for i in range(8):
			r1 = ip[1]
			r2 = ip[2]
			r3 = ip[3]
			r4 = ip[4]
			r5 = ip[5]
			r6 = ip[6]
			r7 = ip[7]
			r8 = ip[8]
			
			a = id[0xae4 + st2] & 0x5
			tmp = st + getindex(a)
			ip[1] = id[tmp] ^ r4

			
			a = id[0xae4 + st2] & 0xa
			a = a >> 1
			tmp = st + getindex(a)
			ip[2] = id[tmp] ^ r7

			a = id[0xae4 + st2] & 0x50
			a = ((a&0xf0) >> 4 ) ^ ((a&0xf) << 4)
			a = a & 0xf
			tmp = st + getindex(a)
			ip[3] = id[tmp] ^ r3

			a = id[0xae4 + st2] & 0xa0
			a = ((a&0xf0) >> 4 ) ^ ((a&0xf) << 4)
			a = a >> 1
			a = a & 0x7
			tmp = st + getindex(a)
			ip[4] = id[tmp] ^ r1

			a = id[0xae4 + st2] & 0x5
			tmp = st + getindex(a)
			ip[5] = id[tmp] ^ r5

			a = id[0xae4 + st2] & 0xa
			a = a >> 1
			tmp = st + getindex(a)
			ip[6] = id[tmp] ^ r6

			a = id[0xae4 + st2] & 0x50
			a = ((a&0xf0) >> 4 ) ^ ((a&0xf) << 4)
			a = a & 0xf
			tmp = st + getindex(a)
			ip[7] = id[tmp] ^ r2

			a = id[0xae4 + st2] & 0xa0
			a = ((a&0xf0) >> 4 ) ^ ((a&0xf) << 4)
			a = a >> 1
			a = a & 0x7
			tmp = st + getindex(a)
			ip[8] = id[tmp] ^ r8

			des = ""

			st += 4
			st2 += 1
		for i in ip[1:]:
			des+= chr(i).encode("hex")+" "
		#print des

		st = 0x100
		st2 = 0

		for i in range(8):
			r1 = ip[1]
			r2 = ip[2]
			r3 = ip[3]
			r4 = ip[4]
			r5 = ip[5]
			r6 = ip[6]
			r7 = ip[7]
			r8 = ip[8]
			a = id[0xae4 + st2] & 0x81
			tmp = st + getindex2(a)
			ip[1] = id[tmp] ^ r4

			
			a = id[0xae4 + st2] & 0x42
			tmp = st + getindex2(a)
			ip[2] = id[tmp] ^ r1

			a = id[0xae4 + st2] & 0x24
			tmp = st + getindex2(a)
			ip[3] = id[tmp] ^ r8

			a = id[0xae4 + st2] & 0x18
			tmp = st + getindex2(a)
			ip[4] = id[tmp] ^ r2

			a = id[0xae4 + st2] & 0x81
			tmp = st + getindex2(a)
			ip[5] = id[tmp] ^ r5

			a = id[0xae4 + st2] & 0x42
			tmp = st + getindex2(a)
			ip[6] = id[tmp] ^ r6

			a = id[0xae4 + st2] & 0x24
			tmp = st + getindex2(a)
			ip[7] = id[tmp] ^ r7

			a = id[0xae4 + st2] & 0x18
			tmp = st + getindex2(a)
			ip[8] = id[tmp] ^ r3

			des = ""

			st2 += 1
			st = st2*4 + 0x100
		for i in ip[1:]:
			des+=chr(i).encode("hex") + " "
		ip[1] = ror(ip[1],8-getrorindex(sums,8,r9)[1])
		ip[2] = ror(ip[2],8-getrorindex(sums,7,r9)[1])
		ip[3] = ror(ip[3],8-getrorindex(sums,6,r9)[1])
		ip[4] = ror(ip[4],8-getrorindex(sums,5,r9)[1])
		ip[5] = ror(ip[5],8-getrorindex(sums,4,r9)[1])
		ip[6] = ror(ip[6],8-getrorindex(sums,3,r9)[1])
		ip[7] = ror(ip[7],8-getrorindex(sums,2,r9)[1])
		des = ""
		for i in ip[1:]:
			des+=chr(i)
		if des[pos - 1] == dest:return ii
                    

for i in range(0x265,0x270):
    des = ""
    tmp = (brute("\xd5",4,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    tmp = (brute("\x7d",1,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    tmp = (brute("\x57",3,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    tmp = (brute("\x72",2,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    
    tmp = (brute("\x78",5,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    tmp = (brute("\x49",6,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    tmp = (brute("\xe6",7,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    
    tmp = (brute("\xf2",8,i & 0xff, (i &0xff00) >> 8 ))
    if tmp:
        des += chr(tmp)
    else: continue
    q = 0
    for a in des:
        q = (q+ord(a))
    
    if q == i:
        print hex(q),hex(i),"\t",des,des.encode("hex")
      
    
		






