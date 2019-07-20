- [1. MySQL](#1-MySQL)
  - [1.1. Storage Engine](#11-Storage-Engine)
  - [1.2. Installation](#12-Installation)
  - [1.3. Data Types](#13-Data-Types)
    - [1.3.1. Các Data types cơ bản](#131-C%C3%A1c-Data-types-c%C6%A1-b%E1%BA%A3n)
    - [1.3.2. Kiểu utf8mb4](#132-Ki%E1%BB%83u-utf8mb4)
  - [1.4. Transaction](#14-Transaction)
    - [1.4.1. Transaction là gì?](#141-Transaction-l%C3%A0-g%C3%AC)
    - [1.4.2. Kiểu transaction](#142-Ki%E1%BB%83u-transaction)
    - [1.4.3. Các thuộc tính Transaction](#143-C%C3%A1c-thu%E1%BB%99c-t%C3%ADnh-Transaction)
    - [1.4.4. Rủi ro của transaction](#144-R%E1%BB%A7i-ro-c%E1%BB%A7a-transaction)
    - [1.4.5. Xử lý transaction](#145-X%E1%BB%AD-l%C3%BD-transaction)
    - [1.4.6. Distributed transaction](#146-Distributed-transaction)
  - [1.5. Isolation](#15-Isolation)
    - [1.5.1. Vấn đề](#151-V%E1%BA%A5n-%C4%91%E1%BB%81)
    - [1.5.2. Read uncommitted](#152-Read-uncommitted)
    - [1.5.3. Read committed](#153-Read-committed)
    - [1.5.4. Repeatable read](#154-Repeatable-read)
    - [1.5.5. Serializable](#155-Serializable)
    - [1.5.6. Snapshot](#156-Snapshot)
    - [1.5.7. Tóm lại](#157-T%C3%B3m-l%E1%BA%A1i)
  - [1.6. Connector](#16-Connector)
    - [1.6.1. JDBC Driver](#161-JDBC-Driver)
    - [1.6.2. Python](#162-Python)

# 1. MySQL

## 1.1. Storage Engine

>Nắm được ưu/nhược điểm của các storage engine cơ bản của MySQL: InnoDB, MyISAM,...

-   Ta sẽ nói qua về Storage Engine, bộ máy lưu trữ của MySQL. Đó thực chất là cách MySQL lưu trữ dữ liệu trên đĩa cứng

-   MySQL lưu trữ mỗi database như là một thư mục con nằm dưới thư mục data. Khi một table được tạo ra, MySQL sẽ lưu định nghĩa bảng ở file đuôi .frm và tên trùng với tên của bảng được tạo. Việc quản lý định nghĩa của bảng là nhiệm vụ của MySQL server. Mỗi storage engine sẽ lưu trữ và đánh chỉ mục (index) dữ liệu khác nhau

-   **InnoDB** là kiểu mặc định và cơ bản nhất của storage engine và Oracle đề xuất sử dụng nó cho các bảng ngoại trừ một vài trường hợp đặc biệt (lệnh **CREATE TABLE** sẽ tạo ra **InnoDB** tables theo mặc định).

-   MySQL Server sử dụng kiến trúc _pluggable storage engine_  để cho phép _storage engines_ được load hoặc không load lên từ MySQL server.

-   Để xác định loại storage engine nào được server hỗ trợ, dùng lệnh **SHOW ENGINES**. Giá trị trong những cột được hỗ trợ sẽ chỉ ra khi nào engine được sử dụng, có gía trị YES hoặc NO hoặc DEFAULT sẽ chỉ ra rằng đã có sẵn, không có sẵn, hoặc có sẵn và hiện tại đang thiết lập mặc định cho storage engine.
   
```sql
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 2. row ***************************
      Engine: MRG_MYISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 4. row ***************************
      Engine: BLACKHOLE
     Support: YES
     Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 7. row ***************************
      Engine: ARCHIVE
     Support: YES
     Comment: Archive storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 8. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 9. row ***************************
      Engine: FEDERATED
     Support: NO
     Comment: Federated MySQL storage engine
Transactions: NULL
          XA: NULL
  Savepoints: NULL
9 rows in set (0.00 sec)

mysql>
```

**MySQL 5.7 hỗ trợ các Storage Engines sau**


**InnoDB**
Đây là Storage Engine mặc định trong MySQL 5.7. **InnoDB** là một Storage Engine transaction-safe (tuân thủ ACID) cho MySQL có các commit, rollback và khả năng khôi phục lỗi để bảo vệ dữ liệu người dùng. Row-level locking của InnoDB và kiểu nonlocking read của Oracle-style làm tăng sự đồng thời và hiệu suất của nhiều người dùng. InnoDB lưu trữ dữ liệu người dùng trong các clustered indexes để giảm I/O cho các truy vấn thông thường dựa trên các primary key. Để duy trì tính toàn vẹn của dữ liệu, InnoDB cũng hỗ trợ các ràng buộc toàn vẹn Foreign Key.

**MyISAM**
Table-level locking giới hạn hiệu suất read/write dữ liệu, vì vậy nó thường được sử dụng cho các công việc read-only hoặc read-mostly trong các cấu hình Web và lưu trữ dữ liệu.

**Memory**
Lưu trữ tất cả dữ liệu trong RAM, để truy cập nhanh trong các môi trường đòi hỏi tra cứu nhanh các dữ liệu không quan trọng. Engine này trước đây gọi là HEAP Engine. Storage Engine này đang sử dụng ít dần, do InnoDB với vùng bộ đệm cung cấp một cách mục đích chung và bền để giữ hầu hết hoặc tất cả dữ liệu trong memory, và NDBCLUSTER cung cấp tra cứu giá trị quan trọng nhanh cho các bộ dữ liệu phân tán lớn.

**CSV**
Các bảng của nó thực sự là các tập tin văn bản với các giá trị được phân cách bởi dấu phẩy. Các bảng CSV cho phép bạn nhập hoặc đổ dữ liệu ở định dạng CSV, để trao đổi dữ liệu với các tập lệnh và ứng dụng đọc và ghi cùng một định dạng. Vì bảng CSV không được lập chỉ mục, bạn thường giữ dữ liệu trong các bảng InnoDB trong quá trình hoạt động bình thường và chỉ sử dụng các bảng CSV trong giai đoạn nhập hoặc xuất.

**Archive**
Các bảng nhỏ gọn, không biểu hiện này được dùng để lưu trữ và truy xuất số lượng lớn các thông tin kiểm tra lịch sử, lưu trữ, hoặc kiểm tra an toàn.

**Blackhole**
Công cụ lưu trữ Blackhole chấp nhận nhưng không lưu dữ liệu, tương tự như `/dev/null` trên Unix. Các truy vấn luôn trả về một tập rỗng. Các bảng này có thể được sử dụng trong các cấu hình nhân bản, nơi các lệnh DML được gửi đến các slave server, nhưng các master server không giữ bản sao dữ liệu của chính nó.

**NDB (NBDCLUSTER)**
Công cụ cơ sở dữ liệu được nhóm lại này đặc biệt phù hợp với các ứng dụng đòi hỏi thời gian hoạt động và tính khả dụng cao nhất có thể.

**Merge**
Cho phép một DBA MySQL hoặc nhà phát triển hợp lý nhóm một loạt các bảng MyISAM giống hệt nhau và tham chiếu chúng như một đối tượng. Tốt cho các môi trường VLDB như lưu trữ dữ liệu.

**Federated**
Cung cấp khả năng liên kết máy chủ MySQL riêng biệt để tạo ra một cơ sở dữ liệu hợp lý từ nhiều máy chủ vật lý. Rất tốt cho môi trường phân phối hoặc môi trường dữ liệu mart.

**Bảng so sánh các storage engine**

Các loại storage engine được cung cấp bởi MySQL được thiết kế để sử dụng tùy theo các trường hợp, bảng sau cung cấp một các nhìn tổng quan về một vài storage engine của MySQL.

| Tính năng 	| InnoDB 	| MyISAM 	| Memory 	| Archive 	| NDB 	|
|-----------------------------------------------	|--------------	|--------	|--------------	|---------	|--------------	|
| Giới hạn lưu trữ 	| 64TB 	| 256TB 	| RAM 	| None 	| 384EB 	|
| Transactions 	| Yes 	| No 	| No 	| No 	| Yes 	|
| Locking granularity 	| Row 	| Table 	| Table 	| Row 	| Row 	|
| MVCC 	| Yes 	| No 	| No 	| No 	| No 	|
| Hỗ trợ kiểu dữ liệu Geospatial 	| Yes 	| No 	| Yes 	| Yes 	| Yes 	|
| Hỗ trợ Geospatial indexing 	| Yes[1] 	| No 	| Yes 	| No 	| No 	|
| B-tree indexes 	| Yes 	| Yes 	| Yes 	| No 	| No 	|
| T-tree indexes 	| No 	| No 	| No 	| No 	| Yes 	|
| Hash indexes 	| No[2] 	| Yes 	| No 	| No 	| Yes 	|
| Full-text search indexes 	| Yes[3] 	| No 	| Yes 	| No 	| No 	|
| Clustered indexes 	| Yes 	| No 	| No 	| No 	| No 	|
| Data caches 	| Yes 	| N/A 	| No 	| No 	| Yes 	|
| Index caches 	| Yes 	| N/A 	| Yes 	| No 	| Yes 	|
| Nén dữ liệu 	| Yes[4] 	| No 	| Yes[5] 	| Yes 	| No 	|
| Dữ liệu được mã hóa[6] 	| Yes 	| Yes 	| Yes 	| Yes 	| Yes 	|
| Hỗ trợ Cluster database 	| No 	| No 	| No 	| No 	| Yes 	|
| Hỗ trợ nhân rộng[7] 	| Yes 	| Yes 	| Yes 	| Yes 	| Yes 	|
| Hỗ trợ khóa ngoại (foreign key) 	| Yes 	| No 	| No 	| No 	| Yes[8] 	|
| Backup / Khôi pục point-in-time[9] 	| Yes 	| Yes 	| Yes 	| Yes 	| Yes 	|
| Hỗ trợ Query cache 	| Yes 	| Yes 	| Yes 	| Yes 	| Yes 	|
| Cập nhật số liệu thống kê cho data dictionary 	| Yes 	| Yes 	| Yes 	| Yes 	| Yes 	|

- [1] InnoDB hỗ trợ cho việc Geospatial indexing từ MySQL 5.7.5 trở lên.
- [2] InnoDB sử dụng Hash index nội bộ cho tính năng Hash Index của nó.
- [3] InnoDB hỗ trợ FULLTEXT từ MySQL 5.6.4 và sau đó.
- [4] Các bảng InnoDB đã nén được yêu cầu định dạng tệp InnoDB Barracuda.
- [5] Các bảng MyISAM nén chỉ được hỗ trợ khi sử dụng định dạng dòng nén. Các bảng sử dụng định dạng nén với MyISAM chỉ được đọc (readonly).
- [6] Thực hiện trên server (thông qua chức năng mã hóa). Mã hóa dữ liệu có sẵn từ MySQL 5.7 trở lên.
- [7] Thực hiện trên server thay vì Storage Engine.
- [8] Hỗ trợ cho khóa ngoại (foreign key) có sẵn từ MySQL Cluster NDB 7.3 và sau đó.
- [9] Thực hiện trên server thay vì Storage Engine.

**InnoDB vs MyISAM**
- InnoDB phục hồi từ một vụ crash hoặc tắt máy bất ngờ bằng cách phát lại các bản ghi log của nó. MyISAM phải quét và sửa chữa đầy đủ hoặc xây dựng lại các chỉ mục hoặc bảng có thể đã được cập nhật nhưng không đầy đủ sang ổ cứng. Kể từ khi phương pháp InnoDB là khoảng thời gian cố định trong khi thời gian MyISAM phát triển với kích thước của các tập tin dữ liệu, InnoDB cung cấp sẵn sàng hơn khi kích thước cơ sở dữ liệu phát triển.
- InnoDB, với innodb_flush_log_at_trx_commit đặt thành 1, ghi nhật ký transaction sau mỗi transaction, cải thiện đáng kể độ tin cậy. MyISAM phải được chạy trên đầu trang của một hệ thống tập tin journal đầy đủ, chẳng hạn như ext4 gắn kết với data=journal, để cung cấp khả năng phục hồi tương tự chống lại các tập tin dữ liệu hỏng. (Journal có thể được đặt trên một thiết bị SSD để cải thiện hiệu năng MyISAM, tương tự, nhật ký InnoDB có thể được đặt trên một hệ thống tập tin không ghi nhật ký như ext2 chạy trên một SSD để tăng hiệu suất tương tự. )
- InnoDB có thể chạy ở chế độ mà nó có độ tin cậy thấp hơn nhưng trong một số trường hợp hiệu năng cao hơn. Thiết lập innodb_flush_log_at_trx_commit đến 0 chuyển sang chế độ mà transaction không commit với disk trước khi kiểm soát được trả lại cho người gọi. Thay vào đó, disk flushes xảy ra trên một bộ đếm thời gian.
InnoDB tự động nhóm lại nhiều chèn đồng thời và flushes chúng vào đĩa cùng một lúc MyISAM dựa vào bộ nhớ cache khối hệ thống tập tin cho bộ nhớ đệm đọc cho các hàng dữ liệu và các chỉ mục, trong khi InnoDB thực hiện điều này trong chính công cụ, kết hợp các cache hàng với các cache chỉ mục.
- InnoDB sẽ lưu trữ các hàng trong trật tự primary nếu có, khác thứ tự duy nhất thứ tự then chốt. InnoDB sẽ sử dụng một phím số nguyên duy nhất được tạo ra bên trong và sẽ lưu trữ các hồ sơ theo thứ tự chèn, vì MyISAM nào. Ngoài ra, một trường khoá chính có thể tự động được sử dụng để đạt được hiệu quả tương tự.
- InnoDB cung cấp lưu trữ trang nén LZW có thể cập nhật cho cả dữ liệu và chỉ mục. MyISAM bảng nén không thể được cập nhật.
Khi hoạt động ở các chế độ tuân thủ ACID đầy đủ, InnoDB phải thực hiện một tuôn ra đĩa ít nhất một lần cho mỗi giao dịch, mặc dù nó sẽ kết hợp flushes cho chèn từ nhiều kết nối. Đối với các ổ cứng hoặc mảng điển hình, điều này sẽ áp đặt giới hạn khoảng 200 giao dịch cập nhật mỗi giây. Đối với các ứng dụng yêu cầu tỷ lệ giao dịch cao hơn, bộ điều khiển đĩa với bộ nhớ đệm ghi và sao lưu pin sẽ được yêu cầu để duy trì tính toàn vẹn của giao dịch. InnoDB cũng cung cấp một số chế độ làm giảm hiệu ứng này, tự nhiên dẫn đến mất bảo đảm toàn vẹn giao dịch, mặc dù vẫn giữ được độ tin cậy cao hơn MyISAM. MyISAM không có chi phí này, nhưng chỉ vì nó không hỗ trợ giao dịch.
- MyISAM sử dụng khóa mức bảng để cập nhật và xóa các hàng hiện có, với một tùy chọn để nối các hàng mới thay vì lấy khóa và chèn chúng vào không gian trống. InnoDB sử dụng khóa cấp hàng. Đối với các ứng dụng cơ sở dữ liệu lớn, nơi nhiều hàng thường được cập nhật, cấp hàng khóa là rất quan trọng bởi vì một khóa bảng duy nhất giảm đáng kể đồng thời trong cơ sở dữ liệu.
Cả InnoDB và MyISAM đều hỗ trợ tìm kiếm toàn văn, với InnoDB đạt được sự hỗ trợ chỉ mục toàn văn trong MySQL 5.6.4, nhưng kết quả có thể khác biệt đáng kể.

## 1.2. Installation

Cài đặt MySQL server, tạo database và table, thao tác với MySQL (select, insert, update, delete, alter) theo link bên dưới
>http://www.ntu.edu.sg/home/ehchua/programming/sql/mysql_howto.html

## 1.3. Data Types

>Nắm được các kiểu dữ liệu cơ bản của MySQL.
>Sử dụng đúng kiểu dữ liệu để đạt hiệu quả tốt nhất.
>Tìm hiểu các dữ liệu đặc biệt và cách xử lý: utf8mb4

### 1.3.1. Các Data types cơ bản

MySQL sử dụng nhiều kiểu dữ liệu, được chia thành 3 loại: kiểu Number, kiểu Datetime, và kiểu String.

- Kiểu dữ liệu Number

  Kiểu dữ liệu| Mô tả
  --|--
  TINYINT(size)|Lưu trữ một số nguyên có giá trị từ -128 đến -127 hoặc 0 đến 255
  SMALLINT(size)| Lưu trữ một số nguyên có giá trị từ -32768 đến 32767 hoặc 0 đến 65535
  MEDIUMINT(size)|Lưu trữ một số nguyên có giá trị từ -8388608 đến 8388607 hoặc 0 đến 16777215
  INT(size)|Lưu trữ một số nguyên có giá trị từ -2147483648 đến 2147483647 hoặc 0 đến 4294967295
  BIGINT(size)|Lưu trữ một số nguyên có giá trị từ -9223372036854775808 đến 9223372036854775807 hoặc 0 đến 18446744073709551615.
  FLOAT(size,d)|Lưu trữ một số thập phân loại nhỏ (Ví dụ: 567.25). Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân.    Tuy nhiên điều này là không bắt buộc, vì mặc định là (10,2).
  DOUBLE(size,d)|Lưu trữ một số thập phân loại lớn. Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân. Mặc định là (16,4).
  DECIMAL(size,d)|Lưu trữ như một chuỗi, cho phép một dấu thập phân cố định. Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân.

- Kiểu dữ liệu String

  Kiểu dữ liệu| Mô tả
  --|--
  CHAR(size)|Dữ liệu kiểu chuỗi có độ dài cố định: Độ dài từ 1 đến 255 kí tự, có thể được chỉ định trước hoặc không
  VARCHAR(size)| Dữ liệu kiểu chuỗi có độ dài thay đổi. Độ dài từ 1 đến 255 kí tự 
  TINYTEXT| Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 255 ký tự
  TEXT| Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 65,535 ký tự
  BLOB| Dùng để lưu trữ dữ liệu nhị phân tối đa là 65,535 byte
  MEDIUMTEXT|Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 16,777,215 ký tự
  MEDIUMBLOB|Dùng để lưu trữ dữ liệu nhị phân tối đa là 16,777,215 byte
  LONGTEXT|Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 4,294,967,295 ký tự
  LONGBLOB|Dùng để lưu trữ dữ liệu nhị phân tối đa là 4,294,967,295 byte
  ENUM|Khi định nghĩa một trường kiểu này, tức là, ta đã chỉ ra một danh sách các đối tượng mà trường phải nhận (có thể là Null). Ví dụ, nếu ta muốn một trường nào đó chỉ nhận một trong các giá trị "A" hoặc "B" hoặc "C" thì ta phải định nghĩa kiểu ENUM cho nó như sau: ENUM ('A', 'B', 'C'). Và chỉ có các giá trị này (hoặc NULL) có thể xuất hiện trong trường đó.

- Kiểu dữ liệu DateTime

  Kiểu dữ liệu| Mô tả
  --|--
  DATE|Một date trong định dạng YYYY-MM-DD, giữa 1000-01-01 và 9999-12-31
  DATETIME|Một tổ hợp Date và Time trong định dạng YYYY-MM-DD HH:MM:SS, giữa 1000-01-01 00:00:00 và 9999-12-31 23:59:59
  TIMESTAMP|Một Timestamp từ giữa nửa đêm ngày 1/1/1970 và 2037 (dạng YYYYMMDDHHMMSS)
  TIME|Lưu time trong định dạng HH:MM:SS
  YEAR(M)|Lưu 1 năm trong định dạng 2 chữ số hoặc 4 chữ số. Nếu độ dài được xác định là 2 (ví dụ: YEAR(2)), YEAR có thể từ 1970 tới 2069 (70 tới 69). Nếu độ dài được xác định là 4, YEAR có thể từ 1901 tới 2155. Độ dài mặc định là 4.

### 1.3.2. Kiểu utf8mb4

 *  Utf8mb4 là kiểu dữ liệu đặc biệt ánh xạ tới từ UTF-8, do đó hỗ trợ đầy đủ Unicode, bao gồm cả các biểu tượng astral.
 *  Đặc điểm
    * Hỗ trợ BMP và các kí tự bổ sung
    * Yêu cầu tối đa 4 byte cho mỗi ký tự nhiều byte

* utf8mb4 tương phản với bộ ký tự utf8mb3, chỉ hỗ trợ các ký tự BMP và sử dụng tối đa ba byte cho mỗi ký tự:
    * Đối với một ký tự BMP, utf8mb4 và utf8mb3 có các đặc tính lưu trữ giống nhau: cùng một giá trị mã, cùng một mã hóa, cùng độ dài. 
    * Đối với một ký tự bổ sung, utf8mb4 yêu cầu bốn byte để lưu trữ nó, trong khi utf8mb3 không thể lưu trữ ký tự đó.

 *  Chuyển đổi `utf8` sang `utf8mb4` trong MySQL
    * Tạo bản sao lưu
    * Nâng cấp MySQL Server phiên bản 5.5.3+
    * Sửa đổi databases, tables, columns

    ```shell
        # For each database:
        ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
        # For each table:
        ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        # For each column:
        ALTER TABLE table_name CHANGE column_name column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        # (Don’t blindly copy-paste this! The exact statement depends on the column type, maximum length, and other properties. The above line is just an example for a `VARCHAR` column.)
    ```

    * Kiểm tra độ dài tối đa của các cột và các khóa chỉ mục: khi chuyển đổi từ utf8 sang utf8mb4, số byte tối đa trong các cột hoặc các khóa không thay đổi, chỉ thay đổi số lượng kí tự do độ dài tối da của mỗi kí tự bây giờ là 4 byte thay vì 3 byte như cũ
    * Sửa đổi bộ kí tự connection, client và server

    ```shell
        mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
        +--------------------------+--------------------+
        | Variable_name            | Value              |
        +--------------------------+--------------------+
        | character_set_client     | utf8mb4            |
        | character_set_connection | utf8mb4            |
        | character_set_database   | utf8mb4            |
        | character_set_filesystem | binary             |
        | character_set_results    | utf8mb4            |
        | character_set_server     | utf8mb4            |
        | character_set_system     | utf8               |
        | collation_connection     | utf8mb4_unicode_ci |
        | collation_database       | utf8mb4_unicode_ci |
        | collation_server         | utf8mb4_unicode_ci |
        +--------------------------+--------------------+
        10 rows in set (0.00 sec)
    ```

    * Sửa chữa và tối ưu hóa các bảng

    ``` shell
        # For each table
        REPAIR TABLE table_name;
        OPTIMIZE TABLE table_name;
    ```



## 1.4. Transaction

Tìm hiểu transaction của MySQL:

- Tại sao phải sử dụng transaction
- Cách sử dụng transaction 
- Xử lý khi gặp lỗi trong transaction 

>https://dev.mysql.com/doc/refman/8.0/en/sql-syntax-transactions.html

### 1.4.1. Transaction là gì?

- Có thể hiểu Transaction là một tiến trình xử lý có xác định điểm đầu và điểm cuối, được chia nhỏ thành các operation (phép thực thi) , tiến trình được thực thi một cách tuần tự và độc lập các operation đó theo nguyên tắc hoặc tất cả đều thành công hoặc một operation thất bại thì toàn bộ tiến trình thất bại. Nếu việc thực thi một operation nào đó bị fail đồng nghĩa với việc dữ liệu phải rollback về trạng thái ban đầu.

- Có thể lấy ví dụ về 1 Transaction đơn giản nhất là tiến trình cài đặt phần mềm hoặc gỡ bỏ phần mềm. Việc cài đặt được chia thành các bước, thực hiện tuần tự từ đầu đến cuối, nếu toàn bộ các bước thực thi thành công đồng nghĩa với việc tiến trình cài đặt hoặc gỡ bỏ phần mềm thành công và ngược lại, một phép thất bại thì tiến trình phải rollback lại tức sẽ không có bất kỳ thay đổi nào trên máy tính.

### 1.4.2. Kiểu transaction 

- Các kiểu transaction khác nhau được phân biệt bằng việc chia các operation như thế nào. Có hai mô hình transaction như sau:
  - **Flat Transaction – Transaction ngang hàng** Việc chia các operation là ngang hàng nhau. Thực thi các operation là tuần tự từ trái sang phải hoặc từ trên xuống dưới.

  - **Nested Transaction – Transaction lồng nhau** Việc thực thi các operation dựa theo nguyên tắc từ trong ra ngoài. Như vậy khi nhìn vào hình vẽ chúng ta thấy các operation ở dạng này có vẻ phụ thuộc vào nhau nhưng khi thực thi thì là độc lập theo nguyên tắc operation trong thực thi xong thì mới đến operation ngoài.

### 1.4.3. Các thuộc tính Transaction

- Mô hình ACID được gắn chặt với cơ sở dữ liệu quan hệ (Relation DB). Tuy nhiên, xét về transaction nói chung, chúng ta cũng có thể áp dụng các thuộc tính này vào.

  - **Atomicity – tính đơn vị:** Một transaction xác định ranh giới của nó rất rõ ràng, tức xác định điểm bắt đầu và kết thúc của tiến trình. Như vậy có thể coi nó như một đơn vị thực thi và đơn vị thực thi này thực hiện theo nguyên tắc “all or nothing”. Nghĩa là nếu một thành phần nào đó trong transaction thực thi hỏng (fail) thì đồng nghĩa với việc không có gì xảy ra tức không có gì thay đổi về mặt dữ liệu.

  - **Consistency – nhất quán:** Dữ liệu nhất quán với transaction ở thời điểm bắt đầu và kết thúc. Nhất quán ở transaction là strong consistency. Để tìm hiểu kỹ hơn về tính nhất quán, xin đọc lại bài viết NoSQL.

  - **Isolation – độc lập:** Nếu hai transaction thực thi cùng lúc thì nguyên tắc thực thi là thực thi độc lập. Nghĩa là một transaction không thể “nhìn thấy” một transaction khác. “Không nhìn thấy” ở đây là không tác động lẫn nhau, chủ yếu trên dữ liệu.

  - **Durability – bền vững:** Dữ liệu của transaction sau khi thực thi xong được cố định, chính thức và bền vững. Nghĩa là những thay đổi đã được cố định, không có chuyện có thể chuyển lại trạng thái dữ liệu lúc trước khi thực hiện transaction.

### 1.4.4. Rủi ro của transaction

- Có ba loại rủi ro chính khiến việc thực thi một transaction có thể bị fail.

  - **Việc thực thi operation bị hỏng:** rõ ràng việc này sẽ dẫn tới transaction bị hỏng. Điều này đã được quy định rõ trong định nghĩa về transaction.

  - **Vấn đề về phần cứng và mạng:** việc phần cứng hoặc mạng có vấn đề trong lúc đang thực thi transaction sẽ dẫn đến tiến trình xử lý thất bại.

  - **Các vấn đề với dữ liệu dùng chung:** Đây là vấn đề khó nhất. Rõ ràng data là một tài nguyên dùng chung, do đó sẽ có những nguy cơ mà transaction gặp phải khi xử lý dữ liệu dùng chung này. Ta sẽ xem xét kỹ hơn dưới đây. Như chúng ta đã biết, phần mềm viết ra là để xử lý dữ liệu, 2 operations (phép) căn bản của phần mềm với dữ liệu là đọc và ghi (read và write) trong đó phép write lại được chia nhỏ thành 3 operations nhỏ hơn là insert (thêm mới), update (sửa), delete (xóa). Dữ liệu là một tài nguyên dùng chung, nếu như có nhiều tiến trình xử lý đồng thời thực hiện các phép trên dữ liệu sẽ xảy ra những rủi ro: write-write, write-read,... việc dữ liệu ghi cùng lúc dẫn tới hỏng dữ liệu hoặc dữ liệu đọc ra không đồng nhất với dữ liệu mới ghi vào,... sẽ đề cập kỹ hơn trong phần tiếp theo dưới đây.

### 1.4.5. Xử lý transaction

>https://viettuts.vn/sql/transaction-trong-sql

- Các lệnh sau đây được sử dụng để xử lý transaction.

  - **COMMIT** – để lưu các thay đổi.
  - **ROLLBACK** – để khôi phục lại các thay đổi.
  - **SAVEPOINT** – tạo ra các điểm trong transaction để ROLLBACK.
  - **SET TRANSACTION** – thiết lập các thuộc tính cho transaction.

- Các lệnh điều khiển transaction chỉ được sử dụng với các lệnh thao tác dữ liệu **DML** như – INSERT, UPDATE và DELETE.

- Chúng không thể được sử dụng trong lệnh CREATE TABLE hoặc DROP TABLE vì các hoạt động này được tự động được commit trong cơ sở dữ liệu.

#### 1.4.5.1. Lệnh COMMIT

- Lệnh COMMIT được sử dụng để lưu các thay đổi gọi bởi một transaction với cơ sở dữ liệu.

- Lệnh COMMIT lưu tất cả các transaction vào cơ sở dữ liệu kể từ khi lệnh COMMIT hoặc ROLLBACK cuối cùng.

- Cú pháp của lệnh COMMIT như sau.

```sql
COMMIT;
```

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau đây:

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------
```

Sau đây là một ví dụ có thể xóa các bản ghi từ bảng có age = 25 và sau đó COMMIT thay đổi trong cơ sở dữ liệu.

```sql
DELETE FROM CUSTOMERS
   WHERE AGE = 25;
COMMIT;
```

Vì vậy, hai hàng từ bảng sẽ bị xóa và câu lệnh SELECT sẽ cho kết quả sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

#### 1.4.5.2. Lệnh ROLLBACK

Lệnh ROLLBACK được sử dụng để hoàn tác các transaction chưa được lưu vào cơ sở dữ liệu. Lệnh này chỉ có thể được sử dụng để hoàn tác các transaction kể từ khi lệnh COMMIT hoặc ROLLBACK cuối cùng được phát hành.

Cú pháp lệnh ROLLBACK như sau:

```sql
ROLLBACK;
```

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau đây:

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

Sau đây là một ví dụ, có thể xóa các bản ghi từ bảng có age = 25 và sau đó XÓA các thay đổi trong cơ sở dữ liệu.

```sql
DELETE FROM CUSTOMERS
   WHERE AGE = 25;
ROLLBACK;
```

Vì vậy, hoạt động xóa sẽ không ảnh hưởng đến bảng và câu lệnh SELECT sẽ cho kết quả sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

#### 1.4.5.3. Lệnh SAVEPOINT

SAVEPOINT là một điểm trong một transaction khi bạn có thể cuộn transaction trở lại một điểm nhất định mà không quay trở lại toàn bộ transaction.

Cú pháp của lệnh SAVEPOINT như thể hiện dưới đây.

```sql
SAVEPOINT SAVEPOINT_NAME;
```

Lệnh này chỉ phục vụ trong việc tạo ra SAVEPOINT trong số tất cả các câu lệnh transaction. Lệnh ROLLBACK được sử dụng để hoàn tác một nhóm các transaction.

Cú pháp để cuộn lại một SAVEPOINT như thể hiện dưới đây.

```sql
ROLLBACK TO SAVEPOINT_NAME;
```

Sau đây là ví dụ bạn định xóa ba bản ghi khác nhau từ bảng CUSTOMERS. Bạn muốn tạo một SAVEPOINT trước mỗi lần xoá, để bạn có thể XÓA trở lại SAVEPOINT bất kỳ lúc nào để trả lại dữ liệu thích hợp cho trạng thái ban đầu.

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

Khối mã sau đây có chứa hàng loạt các hoạt động.

```sql
SQL> SAVEPOINT SP1;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=1;
1 row deleted.
SQL> SAVEPOINT SP2;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=2;
1 row deleted.
SQL> SAVEPOINT SP3;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=3;
1 row deleted.
```

Bây giờ, ba lần xóa đã xảy ra, giả sử rằng bạn đã thay đổi quyết định và quyết định khôi phục lại SAVEPOINT mà bạn đã định nghĩa là SP2. Bởi vì SP2 được tạo ra sau khi xóa đầu tiên, hai lần xóa cuối cùng được khôi phục lại:

```sql
ROLLBACK TO SP2;
Rollback complete.
```

Lưu ý rằng chỉ có lần xoá đầu tiên xảy ra kể từ khi bạn khôi phục lại SP2.

```sql
SELECT * FROM CUSTOMERS;
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
6 rows selected.
```

Lệnh **SAVEPOINT RELEASE**

Lệnh SAVEPOINT RELEASE được sử dụng để loại bỏ một SAVEPOINT mà bạn đã tạo ra.

Cú pháp của lệnh SAVEPOINT RELEASE như sau.

```sql
RELEASE SAVEPOINT SAVEPOINT_NAME;
```

Khi SAVEPOINT bị xóa, bạn không thể sử dụng lệnh ROLLBACK để hoàn tác các transaction được thực hiện kể từ lần SAVEPOINT cuối cùng.

#### 1.4.5.4. Lệnh SET TRANSACTION 

Lệnh SET TRANSACTION có thể được sử dụng để bắt đầu một transaction cơ sở dữ liệu. Lệnh này được sử dụng để chỉ định các đặc tính cho transaction sau. Ví dụ, bạn có thể chỉ định một transaction chỉ được đọc hoặc đọc viết.

Cú pháp cho lệnh SET TRANSACTION như sau.

```sql
SET TRANSACTION [ READ WRITE | READ ONLY ];
```

### 1.4.6. Distributed transaction

>https://en.wikipedia.org/wiki/Distributed_transaction

Một **distributed transaction** (giao dịch phân tán) là một giao dịch **database transaction** được vận hành từ hai hay nhiều host thông qua network. Thông thường, hosts cung cấp một **transactional resources** , trong đó **transaction manager** có trách nhiệm tạo ra và quản lý các global transaction bao gồm các lệnh thao tác với tài nguyên. Distributed transactions cũng như các loại transactions khác phải có 4 tính chất của **ACID** (atomicity, consistency, isolation, duarability).

## 1.5. Isolation

>Xác định isolation level của MySQL để xử lý đồng thời (concurrency)

### 1.5.1. Vấn đề

Giả sử khi chúng ta đang tiến hành song song và đồng thời 2 transaction cùng cập nhật giá trị vào 1 bản ghi trong CSDL. Ở đây sẽ xảy ra **concurency** giữa các transaction và xảy ra các vấn đề :
  1. Transaction trước hay sau sẽ được tiến hành hay cả 2 cùng được tiến hành một lúc.
  2. Kết quả cuối cùng là kết quả của transaction nào trước hay sau? Ở đây xảy ra concurency giữa các transaction, chúng ta cùng tìm hiểu các mức level của **Isolation** để giải quyết vấn đề trên.

### 1.5.2. Read uncommitted

Một transaction lấy dữ liệu từ một transaction khác ngay cả khi transaction đó chưa được commit. Xét ví dụ cụ thể như sau:

Tạo bảng test:

```sql
CREATE DATABASE test;
```

Tạo mới bản ghi:

```sql
INSERT INTO `users` (`id`, `name`, `point`) VALUES ('1', 'Cong', '1');
```

Tiến hành tạo một transaction update point. Query 1:

```sql
START TRANSACTION;
    UPDATE `users` SET `point`= 100;
    SELECT SLEEP(30);
ROLLBACK;
```

Tiến hành Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
	SELECT * FROM `users`;
COMMIT;
```
Giả sử sau khi tiến hành câu Query 1 ta tiến hành chạy câu Query 2 thì kết quả trả về sẽ là 'point' = 100. Nhưng ngay sau khi câu Query 1 chạy xong và bị rollback thì kết quả trả về thực tế sẽ là là 'point' = 1. Như vậy transaction thứ 2 lấy kết quả chưa được commit của transaction thứ 1 => Hiện tượng trên gọi còn được gọi là Dirty Read. Ưu điểm ở đây là các transaction sẽ chạy liên tục và transaction sau ghi đè lên Transaction trước (**Dirty Write**). Đây là mức Isolation thấp nhất và nó cũng tương đương với câu lệnh:

```sql
SELECT * FROM users WITH (nolock)
```

### 1.5.3. Read committed

Đây là level default của một transaction nếu như chúng ta không config gì thêm. Tại level này thì Transaction sẽ không thể đọc dữ liệu từ từ một Transaction đang trong quá trình cập nhật hay sửa đổi mà phải đợi transacction đó hoàn tất. Như vậy thì chúng ta có thể tránh được Dirty Read và Dirty Write nhưng các Transaction sẽ phải chờ nhau => Perfoman hệ thống thấp. Ta thực hiện câu Query 1 như sau:

```sql
START TRANSACTION;
    UPDATE `users` SET `point`= 100 WHERE 'id' > 0;
    SELECT SLEEP(30);
COMMIT;
    SELECT * FROM `users` WHERE `id` = 2;
```

và ngay sau đó thực hiện câu Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
    INSERT INTO `users` (`id`, `name`, `point`) VALUES ('2', 'Vuong', '2');
COMMIT;
```

Khi ta tiến hành thực thi câu Query 2 thì kết quả trả về sẽ bản ghi 'id' = 2 sẽ có point = 2. Mặc dù câu query q1 đã update tất cả bản ghi có id > 0 và updated point = 100 nhưng bản ghi với id = 2 được cập nhật sau khi bảng users được cập nhật và trước khi transaction (q1) kết thúc => Bản ghi này được gọi là **Phantom Row** (Bản ghi ma).


### 1.5.4. Repeatable read

Giống như mức độ của Read Committed, tại mức độ này thì transaction còn không thể đọc / ghi đè dữ liệu từ một transaction đang tiến hành cập nhật trên bản ghi đó. Query 1:

```sql
START TRANSACTION;
    SELECT SLEEP(30);
    SELECT * FROM `users` WHERE `id` = 2;
COMMIT;
```

Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SELECT * FROM `users` WHERE `id` = 2;
COMMIT;
```

Khi thực thi 2 câu query trên thì câu Query 2 phải đợi câu Query 1 commit hoàn tất mới có thể thực thi. Ở level này khi chúng ta sẽ được bảo vệ khi đọc dữ liệu select các bản ghi trong cùng một transaction. Giả sử ở câu Query 2 ta thay thế lệnh select thành lệnh **Update / Delete** thì dữ liệu tại 2 câu query sẽ khác nhau và chúng ta cũng không thể tránh được các **Phantom Row**.

### 1.5.5. Serializable

Level cao nhất của Isolation, khi transaction tiến hành thực thi nó sẽ khóa các bản ghi liên quan và sẽ unlock cho tới khi rollback hoặc commit dữ liệu. Query 1:

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
    SELECT * FROM `users`;
    SELECT SLEEP(30);
    SELECT * FROM `users`;
COMMIT;
```
Query 2:

```sql
INSERT INTO `users` (`id`, `name`, `point`) VALUES ('3', 'Tram', '3');
```

Khi tiến hành 2 câu query trên thì bản ghi trả về giữa 2 lần select ở câu Query 1 là giống như nhau, và câu Query thứ 2 sẽ pending cho tới khi Query 1 kết thúc.


### 1.5.6. Snapshot

Tương tự với level Serializable, nhưng cách thức hoạt động nó lại khác so với Serializable. Khi một transaction select các bản ghi thì nó sẽ không lock các bản ghi này lại, mà tạo một bản sao trên bản ghi hoặc các bản ghi đó. Khi ta tiến hành **UPDATE / DELETE** ta tiến hành trên bản sao dữ liệu đó và không gây ảnh hưởng tới dữ liệu ban đầu. Ưu điểm của snapshot là giảm độ trễ giữa các transaction nhưng bù lại cần tốn thêm tài nguyên lưu trữ các bản sao.

### 1.5.7. Tóm lại

 Transaction isolation level | Dirty reads | Nonrepeatable reads | Phantoms 
---|---|---|---
 **Read uncommitted**	          |       X     |        X            |     X    |
 **Read committed**	          |       -     |        X            |     X    |
 **Repeatable read**		      |       -     |        -            |     X    |
 **Serializable**    	          |       -     |        -            |     -    |


## 1.6. Connector

>Nắm được một số cách kết nối với MySQL: jdbc, python driver,...

### 1.6.1. JDBC Driver

>https://o7planning.org/vi/10167/huong-dan-su-dung-java-jdbc

- **JDBC** (Java Database Connectivity) là một API tiêu chuẩn dùng để tương tác với các loại cơ sở dữ liệu quan hệ. **JDBC** có một tập hợp các class và các Interface dùng cho ứng dụng **Java** có thể nói chuyện với các cơ sở dữ liệu. 

- Các thành phần của **JDBC API** về cơ bản bao gồm:
  - **DriverManager**: Là một class, nó dùng để quản lý danh sách các **Driver** (database drivers). 
  - **Driver**: Là một Interface, nó dùng để liên kết các liên lạc với cơ sở dữ liệu, điều khiển các liên lạc với database. Một khi Driver được tải lên, lập trình viên không cần phải gọi nó một cách cụ thể.
  - **Connection**: Là một Interface với tất cả các method cho việc liên lạc với database. Nó mô tả nội dung liên lạc. tất cả các thông tin liên lạc với cơ sở dữ liệu là thông qua chỉ có đối tượng **Connection**.
  - **Statement**: Là một Interface, gói gọn một câu lệnh SQL gửi tới cơ sở dữ liệu được phân tích, tổng hợp, lập kế hoạch và thực hiện.
  - **ResultSet**: ResultSet đại diện cho tập hợp các bản ghi lấy do thực hiện truy vấn.


- Dùng JDBC kết nối với MySQL:

  - Tạo database sau:
  
  ```sql
    CREATE DATABASE testdb;
    USE testdb;
    CREATE TABLE emplyee (
        id   INT              NOT NULL,
        name VARCHAR (32)     NOT NULL,
        address  VARCHAR (32) NOT NULL,
        PRIMARY KEY (id)
    );

    INSERT INTO employee(id, name, address) VALUES (1, "Cong", "DongNai");
    INSERT INTO employee(id, name, address) VALUES (2, "Vuong", "BenTre");
    INSERT INTO employee(id, name, address) VALUES (3, "Tram", "DaLat");
    INSERT INTO employee(id, name, address) VALUES (4, "Tran", "DaLat")

  ```

  - Tạo **maven** project với **pom.xml** include:

  ```
   <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.6</version>
    </dependency>
  ``` 

  - Viết code kết nối :
  
  ```java
  public class ConnectMysqlExample {
        private static String DB_URL = "jdbc:mysql://localhost:3306/testdb";
        private static String USER_NAME = "root";
        private static String PASSWORD = "cong";

        public static void main(String args[]) {
            try {
                // connnect to database 'testdb'
                Connection conn = getConnection(DB_URL, USER_NAME, PASSWORD);
                // crate statement
                Statement stmt = conn.createStatement();
                // get data from table 'employee'
                ResultSet rs = stmt.executeQuery("select * from employee");
                // show data
                while (rs.next()) {
                    System.out.println(rs.getInt(1) + "  " + rs.getString(2) 
                            + "  " + rs.getString(3));
                }
                // close connection
                conn.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }

    public static Connection getConnection(String dbURL, String userName, 
                String password) {
            Connection conn = null;
            try {
                Class.forName("com.mysql.jdbc.Driver");
                conn = DriverManager.getConnection(dbURL, userName, password);
                System.out.println("connect successfully!");
            } catch (Exception ex) {
                System.out.println("connect failure!");
                ex.printStackTrace();
            }
            return conn;
        }
    }

  ```

  - Kết quả :
  
  ```
   connect successfully!
    1  Cong  DongNai
    2  Vuong  BenTre
    3  Tram  DaLat
    4  Tran  DaLat
  ```

### 1.6.2. Python

- Dùng `mysql.connector` trên python:
  - Install module :

  ```sh
    python -m pip install mysql-connector
  ```

  - Viết code python:

  ```py
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="cong",
        database="testdb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM employee")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
  ```

  - Kết quả :

  ```
  $ python b.py
    (1, u'Cong', u'DongNai')
    (2, u'Vuong', u'BenTre')
    (3, u'Tram', u'DaLat')
    (4, u'Tran', u'DaLat')
  ```
