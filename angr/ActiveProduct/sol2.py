import angr
import logging


#logging.getLogger('angr.path_group').setLevel(logging.DEBUG)

def get_byte(s, i):
    pos = s.size() / 8 - 1 - i
    return s[pos * 8 + 7 : pos * 8]

exe = '76.elf'
start_ = 0x4005bf # before call
good = 0x000000400724 # call print flag
mem = 0x006042C0

flag_len = 0x43

p = angr.Project(exe,load_options={"auto_load_libs":False})

state = p.factory.blank_state(addr=start_)

argv=[exe, state.se.BVS('arg1', flag_len*8)]
s = state
s.mem[mem:] = argv[1]

for i in xrange(flag_len):
    # We want those flags to be printable characters
    byte = get_byte(argv[1], i)
    state.add_constraints(byte >= 0x20)
    state.add_constraints(byte <= 0x7e)

path = p.factory.path(state=state)

ex = p.surveyors.Explorer(start=path, find=(good, ))
ex.run()

possible_flags = ex.found[0].state.se.any_n_int(argv[1],20)

for f in possible_flags:
	print hex(f)[2:-1].decode("hex")

