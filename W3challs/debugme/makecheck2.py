fic = open("check_gcc.asm").read()
for l in fic.split("\n"):
    print '"%s;"' %l
