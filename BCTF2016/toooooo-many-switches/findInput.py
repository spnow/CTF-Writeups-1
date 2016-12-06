from struct import pack,unpack
base = 0x79cf60
start = 0x440d
f = open("samples","w")
def fix(a):
	if a[-1] == "h":
		a = a[:-1]
	return a
def trace(current, Flag):
	if GetOpnd(current,1) == "0FFFFFFFFFFFFFFFFh":
		return
	
	current = NextHead(current)
	
	if GetMnem(current) == "add":
		tmp = current
		add = int(fix(GetOpnd(tmp,1)),16)
		tmp = NextHead(NextHead(tmp))
		ran = int(fix(GetOpnd(tmp,1)),16)
		
		tmp = NextHead(NextHead(tmp))
		tmp = NextHead(NextHead(tmp))
		tmp = NextHead(tmp)
		
		bas = int(GetOpnd(tmp,1)[7:-7],16)
		st = (0-add) & 0xff
		fn = st + ran
		for i in range(st,fn+1):
			sOff = ((i + add) & 0xff)*8 + bas
			sDat = unpack("<Q",get_many_bytes(sOff,8))[0]
			
			if GetOpnd(sDat,1) == "0FFFFFFFFFFFFFFFFh":
				continue
			nOff = int(fix(GetOpnd(sDat,1)),16)*8 + base
			nDat = unpack("<Q",get_many_bytes(nOff,8))[0]
			trace(nDat,Flag + chr(i))
			
	if GetMnem(current) == "sub":
		tmp = current
		key = int(fix(GetOpnd(current,1)),16)
		while GetOpnd(tmp,0) != "dword ptr [rbp-24h]":
			tmp = NextHead(tmp)
		tOpn = GetOpnd(tmp,1)
		if tOpn[-1] == "h":
			tOpn = tOpn[:-1]
		nOff = int(tOpn,16)*8 + base +0 +0
		nDat = unpack("<Q",get_many_bytes(nOff,8))[0]
		
		if chr(key) == "}":
			tmp2 = nDat
			while (GetOpnd(tmp2,0) != "dword ptr [rsp+0]"):
				tmp2 = NextHead(tmp2)
			if int(fix(GetOpnd(tmp2,1)),16) == 4:
				print Flag+chr(key)
				f.write(Flag+chr(key)+ "\n")
			return
		trace(nDat,Flag+chr(key))
	
	if GetMnem(current) == "mov":
		al = []
		tmp = current
		while True:
			if GetMnem(tmp) == "sub":
				al.append(tmp)
			if GetMnem(tmp) == "jz":
				sTmp = int(GetOpnd(tmp,0)[4:],16)
				if GetOpnd(sTmp,1) == "0FFFFFFFFFFFFFFFFh":
					break
		
			if GetOpnd(tmp,1) == "0FFFFFFFFFFFFFFFFh":
				break
			
			tmp = NextHead(tmp)
		
		for i in al:
			tmp = i
			key = int(fix(GetOpnd(i,1)),16)
			
			while GetMnem(tmp)[0] != "j":
				tmp = NextHead(tmp)
				
			if GetMnem(tmp) == "jz":
				sDat = int(GetOpnd(tmp,0)[4:],16)
			elif GetMnem(tmp) == "jnz":
				sDat = NextHead(NextHead(tmp))
				
			tOpn = GetOpnd(sDat,1)
			if tOpn[-1] == "h":
				tOpn = tOpn[:-1]		
			nOff = int(tOpn,16)*8 + base +0
			nDat = unpack("<Q",get_many_bytes(nOff,8))[0]
			trace(nDat,Flag + chr(key))
				
trace(0x400b0f,"")
f.close()
#BCTF{piYqQQ4EjJNs6<wL}