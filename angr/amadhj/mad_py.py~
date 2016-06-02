import angr
import logging


#logging.getLogger('angr.path_group').setLevel(logging.DEBUG)

def get_byte(s, i):
    pos = s.size() / 8 - 1 - i
    return s[pos * 8 + 7 : pos * 8]

exe = 'mad2'
start_ = 0x4029C5 # before call
bad = 0x0000004029D8 # skipped over
good = 0x0000004029D3 # call print flag
mem = 0x006042C5

flag_len = 32

p = angr.Project(exe,load_options={"auto_load_libs":False})

state = p.factory.blank_state(addr=start_)
state.regs.rdi = mem
s = state
argv=[exe, state.se.BVS('arg1', flag_len*8)]

s.mem[mem:] = argv[1]

for i in xrange(flag_len):
    # We want those flags to be printable characters
    byte = get_byte(argv[1], i)
    state.add_constraints(byte >= ord(' '))
    for j in xrange(ord(' ') + 1, ord('@') + 1):
        state.add_constraints(byte != j)
    state.add_constraints(byte <= ord('z'))
    state.add_constraints(byte != ord(']'))
    state.add_constraints(byte != ord('\\'))
    state.add_constraints(byte != ord('^'))
    state.add_constraints(byte != ord('`'))
    state.add_constraints(byte != ord('['))

path = p.factory.path(state=state)

ex = p.surveyors.Explorer(start=path, find=(good, ), avoid=(bad,))
ex.run()

possible_flags = ex.found[0].state.se.any_n_int(argv[1],20)

for f in possible_flags:
	print hex(f)[2:-1].decode("hex")

