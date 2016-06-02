import angr
import logging
import claripy
logging.getLogger('angr.path_group').setLevel(logging.DEBUG)
exe = '76.elf'
start_ = 0x4005bf # before call
good = 0x000000400724 # call print flag
mem = 0x006042C0

flag_len = 0x43

p = angr.Project(exe,load_options={"auto_load_libs":False})
flag = claripy.BVS( 'flag',0x43 * 8)
state = p.factory.blank_state(addr=start_)
state.mem[mem] = flag
for i in flag.chop(8):
	state.add_constraints(i != 0)



path = p.factory.path(state=state)

ex = p.surveyors.Explorer(start=path, find=(good))
ex.run()

state = ex.found[0].state
for i in range(8):
	b = state.memory.load(mem+i,1)
	state.add_constraints(b >=0x21, b<=0x7e)

print hex(state.se.any_int(state.memory.load(0x6042C0, 0x43)))[2 :-1].decode( 'hex').strip(' \0')
