Bài này cho chúng ta chọn số rất lớn nhưng khi lấy index lại thực hiện AND index với 0xFF, nên chúng ta có thể chọn nhiều số khác nhau nhưng khi lấy index lại giống nhau.

Lợi dụng hàm atoi() có return value là signed int, nhưng khi lấy kết quả lại sử dụng unsigned int, ta cho range của index là từ 1 đến -1 thì kết quả sẽ là từ 1 đến 0xFFFF, số lượng tối đa có thể chọn.

Ngoài ra, chương trình còn cho chúng ta nhập fixed ending cho index, nên ta điền số bất kỳ cho đủ 12byte input, vậy nếu input của chúng ta là [1--1]000000 thì index sẽ lấy từ 1000000 đến 65535000000.

Một điều cần chú ý nữa về hàm atoi() là nếu string input là hợp lệ nhưng lại nằm ngoài range của signed int thì return value sẽ là INT_MAX (2147483647) hoặc INT_MIN (-2147483648), mà index tối đa của chúng ta tới 65535000000, lớn hơn INT_MAX rất nhiều nên đa số trường hợp index sẽ là INT_MAX và AND với 0xFF bằng 2147483647 & 0xFF = 0xFF. Ta cũng có thể tính số lần index = 0xFF như sau: (65535 - 2147) * 6 = 380328, đủ để thỏa yêu cầu lớn hơn 78704 của đề bài.

Như vậy, để có được flag, ta sẽ nhập input là 6 lần [1--1]000000 và tìm cách sao cho 5 lần random() % 1024 có ít nhất 1 lần có giá trị 0xFF, để làm được điều này ta liệt kê tất cả các seed cho ra giá trị random tương ứng và chạy payload đúng thời điểm thích hợp.