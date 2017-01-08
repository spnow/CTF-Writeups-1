rem nasm -f coff check.asm
gcc -o debug.exe -Wall -s main.c debugfun.c globals.c check.o -lgdi32 -lpsapi -mwindows

