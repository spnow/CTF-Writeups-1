from ctypes import c_uint64
 
secret_table = []
 
for i in range(256):
 t = c_uint64(i)
 for _i in range(8):
  b = t.value & 0x1
  t.value = t.value >> 0x1
  if b:
   t.value ^= 0xc96c5795d7870f42
 
 secret_table.append( t.value )

 
init_value = '_[Hello___Welcome To Reversing.Kr]__The idea of the algorithm came out of the codeengn challenge__This algorithm very FXCK__But you can solve it!!__Impossible is Impossible_()_[]_()_[]_()_[]_()_[]_()_[]_()_[]\xe7\x51\xde\x35\xa3\x13\x90\x2e)_[]_()_[]_()_[]_()_[]_()_[]_()_[]_()_[\x00'
 
key = '01234567'
 
input_value = list(init_value)
for e,i in enumerate(key):
 input_value[e*0x10] = i
print input_value
r = c_uint64(0)
for i in input_value:
 idx = ord(i)^(r.value & 0xff)
 r.value = r.value >> 8
 r.value ^= secret_table[ idx ]
 
 print hex(r.value)
if r.value == 0x676f5f675f695f6c:
 print 'wow get'
 print hex(r.value)