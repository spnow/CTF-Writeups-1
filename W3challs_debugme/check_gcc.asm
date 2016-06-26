push %eax
add %ebx,%eax
shl %eax
inc %ebx
pop %eax
dec %ebx
.byte $0xCC .byte $0x23
push %ebp
mov %esp,%ebp
.byte $0xCC .byte $0xb7 .byte $0xaa .byte $0x40 .byte $0x00 .byte $0x55 .byte $0xC3
push %ebx
lea 8(%ebp), %ebx
movl (%ebx),%ebx
movl (%ebx),%eax
xor $0xCC9B402A, %eax
rol %eax
.byte $0xCC .byte $0x9b .byte $0xbb .byte $0x9a .byte $0x3e .byte $0xf0 .byte $0xb4 .byte $0x49
sub 0xffbdd1f7,%eax
mov %eax,%ecx
mov 4(%ebx),%eax
.byte $0xcc .byte $0xf2 .byte $0x78 .byte $0xfa .byte $0xd .byte $0xe3
mov %eax,%edx
shl %edx
add %eax,%edx
.byte $0xcc .byte $0x69 .byte $0x9d .byte $0xe1
add $0x6363e154,%edx
xor %eax,%eax
or %ecx,%edx
jne end
.byte $0xcc .byte $0xc1
movw 8(%ebx), %dx
cmp $105, %dx
jne end
inc %eax
end:pop %ebx
    pop %ebp
    ret
.byte $0x9D .byte $0x9a .byte $0xf5 .byte $0x7c .byte $0xd .byte $0x54 .byte $0x6f .byte $0x93