
#!/usr/bin/python

import angr
import simuvex

def main():
	print '[*] Loading file...'

	# Create a new project, do not load shared libs
	proj = angr.Project('amadhj', load_options={'auto_load_libs': False})

	print '[*] Setting up initial state'
	#files = {'/dev/stdin': simuvex.storage.file.SimFile("/dev/stdin", "r", size=32)}
	# Create a blank state at the start of check function
	initial_state = proj.factory.blank_state(addr=0x4026d1, remove_options={simuvex.o.LAZY_SOLVES})
	#initial_state = proj.factory.entry_state(fs=files, concrete_fs=True)
	# The flag is a bit vector containing 30 bytes, each byte contains 8 bits
	

	# Setup return address
	#initial_state.mem[initial_state.regs.esp].dword = 0x8049A49

	# path from the state
	initial_path = proj.factory.path(initial_state)
	
	# Veritesting is important to avoid unnecessary branching and path explosion
	# Read more here: https://users.ece.cmu.edu/~aavgerin/papers/veritesting-icse-2014.pdf
	exp = angr.surveyors.Explorer(proj, start=initial_path, find=(0x4027ea,),  enable_veritesting=True)

	print '[*] Finding the flag, please wait...'

	# GO, Go, go ...
	result = exp.run()

	if result.found:
		found_state = result.found[0].state
		print '\nFlag is:', result.found[0].state.posix.dumps(0)

if __name__ == '__main__':
	# Enable logging
	angr.path_group.l.setLevel("DEBUG")
	main()
