Đầu tiên, chương trình yêu cầu 4 tham số là 4 số hệ 10, sau đó 4 số này được lưu liền nhau vào 1 array A 16 bytes.
Tiếp theo định nghĩa Unhandled Exception tại hàm sub_4013D0
Để tiện phân tích, ta build các biến trong sub_4013D0 theo struct EXCEPTION_POINTERS

Tiếp tục trace, thì ta gặp exception 0xC0000005 EXCEPTION_ACCESS_VIOLATION, tham khảo trong hàm sub_4013D0 thì khi lần đầu gặp exception này, EIP được set = sub_4015e0

Tiếp tục trace sub_4015e0, ta gặp exception 0xC0000094 EXCEPTION_INT_DIVIDE_BY_ZERO tại lệnh div eax, handler của exception này kiểm tra xem esi có == 64 hay không, nếu có thì EIP += 21, nếu không EIP += 2

Tiếp tục trace sub_4015e0, ta gặp exception 0xC000001D EXCEPTION_ILLEGAL_INSTRUCTION tại lệnh ud2 ??, handler của exception này set EIP -= 21 và tăng esi += 4

Như vậy cặp 2 exception trên tạo thành một vòng lặp 64/4 = 16 lần, mục đích sao chép từng byte của array A vào array B, khi esi == 64 thì eip += 21 tức địa chỉ thực thi tiếp theo là 0x4015FB

Đoạn code tiếp theo tạo 0x4015FB thực hiện lấy một byte trong array B nhân với một byte hardcode array C, kết quả lưu vào ebx, sau đó gặp exception 0xC0000096 EXCEPTION_PRIV_INSTRUCTION. Nội dung cơ bản của handler này là tạo thành vòng lặp lấy từng cặp 4byte của array B nhân với cặp 4byte của array C, tổng lại đem so sách với một số hardcode array D, kết quả lưu vào array E.

sau đó thì exception 0xC0000005 được gọi lần 2, set eip đến hàm sub_4012a0,
hàm này đơn giản kiểm tra array E có = 1 hết không và in ra flag xor-ed với array A.

như vậy, để tìm được 4 argv ta phải giải hệ phương trình

0x33 x a0 + 0x7B x b0 + 0x67 x c0 + 0xBB x d0 = 0x11F3E

0x33 x a1 + 0x7B x b1 + 0x67 x c1 + 0xBB x d1 = 0x738F

0x33 x a2 + 0x7B x b2 + 0x67 x c2 + 0xBB x d2 = 0xDCAC

0x33 x a3 + 0x7B x b3 + 0x67 x c3 + 0xBB x d3 = 0x2ABD

.

.

.

.

.


dùng Z3 ta được 4 argv lần lượt là: 305668685 541343641 24669363 548417709
