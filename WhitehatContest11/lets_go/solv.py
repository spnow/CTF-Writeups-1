def calc(input):
    array_A = [0x1, 0x1, 0x2, 0x6, 0x18, 0x78, 0x2D0, 0x013B0, 0x09D80, 0x58980, 0x00375F00, 0x02611500, 0x1C8CFC00]

    array_B = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    rsi = len(input)
    rdi = 1
    r10 = rsi + 1
    for rcx in range(1, r10):
        rbx = array_B[input[rcx - 1]] - 1
        rbp = array_A[rsi - rcx]
        rbx *= rbp
     
        rdi += rbx
        
        rax = input[rcx-1] + 1
        while rax <= rsi:
            array_B[rax] -= 1
            rax = rax + 1
    return rdi

des = 0x0E37F550
ip_list = [1,2,3,4,5,6,7,8,9,10,11,12]
st_list = [1]*12
for i in range(12):
    tmp = ip_list[0]
    for j in ip_list:
        st_list[i] = j
        if calc(st_list) > des:
            st_list[i] = tmp
            ip_list.remove(tmp)
            break
        tmp = j

print st_list
