# Redis

## Version

Nắm được các version của redis, đặc biệt các version chạy ổn định (stable)

https://redis.io/download

Redis uses a standard practice for its versioning: major.minor.patchlevel. An even minor marks a stable release, like 1.2, 2.0, 2.2, 2.4, 2.6, 2.8. Odd minors are used for unstable releases, for example 2.9.x releases are the unstable versions of what will be Redis 3.0 once stable.

## Installation


Cài đặt redis server: single và cluster 

https://redis.io/topics/quickstart

https://redis.io/topics/cluster-tutorial

### Cài đặt Redis server : Single

* Download, extract và compile Redis với:
    ``` shell
        $ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
        $ tar xzf redis-5.0.2.tar.gz
        $ cd redis-5.0.5
        $ make
    ```

* Các tệp nhị phân hiện được biên dịch có sẵn trong thư mục src. Chạy Redis server:
    ``` shell
        $ src/redis-server
    ```
* Tương tác với Redis bằng ứng dụng được tích hợp sẵn
    ``` shell
        $ src/redis-cli
        redis> set foo bar
        OK
        redis> get foo
        "bar"
    ```

### Cài đặt Redis server: Cluster

- Tạo 6 node, gồm 3 master và 3 slave, tạo 6 file config trong 6 thư mục từ 7000 đến 7005

```
$ mkdir 7000 7001 7002 7003 7004 7005
$ touch 7000/redis.conf  
```
- Trong mỗi file conf, có nội dung tương tự như sau,(khác nhau tên port)

```
port 7000
cluster-enabled yes
daemonize yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```
- Tạo file start.sh như sau :

```
cd ~/redis-cluster/7000/ && redis-server redis.conf
cd ~/redis-cluster/7001/ && redis-server redis.conf
cd ~/redis-cluster/7002/ && redis-server redis.conf
cd ~/redis-cluster/7003/ && redis-server redis.conf
cd ~/redis-cluster/7004/ && redis-server redis.conf
cd ~/redis-cluster/7005/ && redis-server redis.conf
```

- Tạo cluster :

```
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 \
127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
--cluster-replicas 1
```

- Bật redis-cli để kiểm tra, chỉ thị -c để redis-cli tự động chuyển cửa sổ sang cli bên port khác.

```
$ redis-cli -p 7000 -c
```


## Các lệnh cơ bản và quản lý dữ liệu trong Redis

Nắm được các kiểu dữ liệu của Redis 

https://redis.io/topics/data-types-intro 

Làm quen với các lệnh trong Redis 

https://try.redis.io/


### Redis Keys

Redis key là các lệnh sử dụng để quản lý các key trong redis. Với cú pháp như sau:

```
COMMAND KEY_NAME [VALUE]
```

**Các lệnh thường dùng**

| STT 	| Command 	| Ý nghĩa 	|
|-----	|---------------------	|------------------------------------------------------------------------------------------------	|
| 1 	| DEL key 	| Xóa key nếu nó tồn tại 	|
| 2 	| EXISTS key 	| Kiểm tra key có tồn tại không 	|
| 3 	| EXPIRE key n 	| Đặt expire time cho key sau n giây 	|
| 4 	| KEYS pattern 	| Tìm các key theo pattern 	|
| 5 	| PERSIST key 	| Xóa expire time của key 	|
| 6 	| TTL key 	| Lấy thời gian sống của key (giây) 	|
| 7 	| RENAME key newkey 	| Đổi tên key sang newkey, nếu newkey đã tồn tại giá trị của nó sẽ bị ghi đè bởi giá trị của key 	|
| 8 	| RENAMENX key newkey 	| Đổi tên key sang newkey nếu newkey chưa tồn tại 	|
| 9 	| TYPE key 	| Lấy loại dữ liệu được lưu trữ bởi key 	|

### Redis String

Redis string là lệnh sử dụng để quản lý các key/value trong đó value có giá trị string trong redis

```redis
redis 127.0.0.1:6379> SET test redis
OK
redis 127.0.0.1:6379> GET test
"redis"
```
**Các lệnh thường dùng**

| STT 	| Command 	| Ý nghĩa 	|
|-----	|-------------------------	|---------------------------------------------------	|
| 1 	| SET key value 	| Đặt giá trị value cho key 	|
| 2 	| GET key 	| Lấy giá trị lưu trữ bởi key 	|
| 3 	| GETRANGE key start end 	| Lấy giá trị lưu trữ bởi key từ (start) đến (end) 	|
| 4 	| GETSET key value 	| Lấy ra giá trị cũ và đặt giá trị mới cho key 	|
| 5 	| MGET key1 key2 .. 	| Lấy giá trị của nhiều key theo thứ tự 	|
| 6 	| SETEX key seconds value 	| Đặt giá trị và thời gian expire cho key 	|
| 7 	| SETNX key value 	| Đặt giá trị cho key nếu key chưa tồn tại 	|
| 8 	| RENAMENX key newkey 	| Đổi tên key sang newkey nếu newkey chưa tồn tại 	|
| 9 	| STRLEN key 	| Lấy độ dài giá trị lưu trữ bởi key 	|
| 9 	| APPEND key value 	| Thêm vào sau giá trị lưu trữ bởi key là value 	|
| 10 	| INCR key 	| Tăng giá trị lưu trữ của key (số nguyên) 1 đơn vị 	|
| 11 	| INCRBY key n 	| Tăng giá trị lưu trữ của key (số nguyên) n đơn vị 	|
| 12 	| DECR key 	| Giảm giá trị lưu trữ của key (số nguyên) 1 đơn vị 	|
| 11 	| DECRBY key n 	| Giảm giá trị lưu trữ của key (số nguyên) n đơn vị 	|


### Redis Hash

Redis hash là lệnh sử dụng để quản lý các key/value trong đó value có giá trị là hash. Hash là kiểu dữ liệu khá phổ biến, thường được dùng để lưu trữ các object.

```redis
HSET user:1 name "name 1"
(integer) 1
HGET user:1 name
"name 1"
```

**Các lệnh thường dùng**

| STT 	| Command 	| Ý nghĩa 	|
|-----	|-------------------------------------------	|---------------------------------------------------------------------	|
| 1 	| HSET key field value 	| Đặt giá trị cho field là value trong hash 	|
| 2 	| HGET key field 	| Lấy giá trị của field trong hash 	|
| 3 	| HDEL key field1 field2 ... 	| xóa field1, field2 ... trong hash 	|
| 4 	| HEXISTS key field 	| Kiểm tra file có tồn tại trong hash không 	|
| 5 	| HGETALL key 	| Lấy tất cả các field và value của nó trong hash 	|
| 6 	| HINCRBY key field n 	| Tăng giá trị của field (số nguyên) lên n đơn vị 	|
| 7 	| HDECRBY key field n 	| Giảm giá trị của field (số nguyên) lên n đơn vị 	|
| 8 	| HINCRBYFLOAT key field f 	| Tăng giá trị của field (số thực) lên f 	|
| 9 	| HDECRBYFLOAT key field n 	| Giảm giá trị của field (số thực) f 	|
| 10 	| HKEYS key 	| Lấy tất cả các field của hash 	|
| 11 	| HVALS key 	| Lấy tất cả các value của hash 	|
| 12 	| HLEN key 	| Lấy số lượng field của hash 	|
| 13 	| HMSET key field1 value1 field2 value2 ... 	| Đặt giá trị cho các field1 giá trị value1 field2 giá trị value2 ... 	|
| 14 	| HMGET key field1 field2 ... 	| Lấy giá trị của các field1 field2 ... 	|

### Redis list

Redis list là lệnh sử dụng để quản lý các key/value trong đó value có giá trị là một list (danh sách). List là kiểu dữ liệu khá phổ biến, có 2 kiểu list thường dùng là stack (vào sau ra trước) và queue (vào trước ra trước)

```
LPUSH test value1
 (integer) 1
 LPUSH test value2
 (integer) 2
 LPUSH test value3
 (integer) 3
 LRANGE test 0 10
1) "value1"
2) "value2"
3) "value3"
```

**Các lệnh thường dùng**

| STT 	| Command 	| Ý nghĩa 	|
|-----	|----------------------------------	|---------------------------------------------------------------------	|
| 1 	| LINDEX key index 	| Lấy giá trị từ danh sách (list) ở vị trí index (index bắt đầu từ 0) 	|
| 2 	| LLEN key 	| Lấy số lượng phần tử trong danh sách 	|
| 3 	| LPOP key 	| Lấy phần tử ở đầu danh sách 	|
| 4 	| LPUSH key value1 value2 ... 	| Thêm value1 value2... vào đầu danh sách 	|
| 5 	| LRANGE key start stop 	| Lấy các phần tử trong list từ vị trí start đến vị trí stop 	|
| 6 	| LSET key index value 	| Đặt lại giá trị tại index bằng value 	|
| 7 	| RPOP key 	| Lấy giá trị ở cuối danh sách 	|
| 8 	| RPUSH key value1 value2 ... 	| Thêm phần tử value1 value2 ... vào cuối danh sách 	|
| 9 	| LINSERT key BEFORE value1 value2 	| Thêm phần tử value2 vào trước phần tử value1 trong danh sách 	|
| 10 	| LINSERT key AFTER value1 value2 	| Thêm phần tử value2 vào sau phần tử value1 trong danh sách 	|

### Redis Set

Redis set là lệnh sử dụng để quản lý các key/value trong đó value có giá trị là một set (tập hợp). Các giá trị trong tập hợp là duy nhất không bị trùng lặp.

```
redis 127.0.0.1:6379> SADD test value1
(integer) 1
redis 127.0.0.1:6379> SADD test value2
(integer) 1
redis 127.0.0.1:6379> SADD test value3
(integer) 1
redis 127.0.0.1:6379> SADD test value4
(integer) 0
redis 127.0.0.1:6379> SMEMBERS test

1) "value1"
2) "value2"
3) "value3"
```

**Các lệnh thường dùng**

| STT 	| Command 	| Ý nghĩa 	|
|-----	|---------------------------	|--------------------------------------------------------------------------	|
| 1 	| SADD key value1 value2 .. 	| Thêm các giá trị value1 value2 ... vào tập hợp 	|
| 2 	| SCARD key 	| Lấy số lượng phần tử trong tập hợp 	|
| 3 	| SMEMBERS key 	| Lấy các phần tử trong tập hợp 	|
| 4 	| SPOP key 	| Xóa bỏ ngẫu nhiên một phần tử trong tập hợp và trả về giá trị phần tử đó 	|

### Redis sorted sets

Redis sorted set là lệnh sử dụng để quản lý các key/value trong đó value có giá trị là một sorted set (tập hợp được sắp xếp theo điểm/độ ưu tiên từ thấp đến cao). Các giá trị trong sorted set là duy nhất không bị trùng lặp.

```
redis 127.0.0.1:6379> ZADD test 1 value1
(integer) 1
redis 127.0.0.1:6379> ZADD test 3 value2
(integer) 1
redis 127.0.0.1:6379> ZADD test 2 value3
(integer) 1
redis 127.0.0.1:6379> ZADD test 4 value4
(integer) 0
redis 127.0.0.1:6379> ZADD test 5 value4
(integer) 0
redis 127.0.0.1:6379> ZRANGE test 0 10 WITHSCORES

1) "value1"
2) "1"
3) "value3"
4) "2"
5) "value2"
6) "3"
7) "value4"
8) "5"
```

**Các lệnh thường dùng**


| STT 	| Command 	| Ý nghĩa 	|
|-----	|-----------------------------------------	|--------------------------------------------------------------------------------------------	|
| 1 	| ZADD key score1 value1 score2 value2 .. 	| Thêm các phần tử value1 value2 vào sorted set với độ ưu tiên tương ứng là score1 và score2 	|
| 2 	| SCARD key 	| Lấy số lượng phần tử trong sorted set 	|
| 3 	| ZRANGE key start stop 	| Lấy các phần tử trong tập hợp từ start đến stop 	|
| 4 	| ZRANGE key start stop WITHSCORES 	| Lấy các phần tử trong tập hợp từ start đến stop kèm theo giá trị score của chúng 	|
| 5 	| ZSCORE key member 	| Lấy giá trị score của member 	|
| 6 	| ZRANK key member 	| Lấy vị trí của member trong sorted set 	|
| 7 	| ZCOUNT key score1 score2 	| Đếm số member có score tương ứng trong đoạn score1 đến score2 	|

### Redis transaction

Một điểm khá thú vị trong Redis là transaction. Redis transaction cho phép một nhóm các lệnh thực hiện theo thứ tự cho đến khi lệnh cuối cùng được thực hiện xong. Khi này Redis mới cập nhật đồng thời dữ liệu thay đổi bởi nhóm lệnh này. Redis transaction bắt đầu bằng lệnh MULTI và kết thúc bằng lệnh EXEC


```
redis 127.0.0.1:6379> MULTI
OK
redis 127.0.0.1:6379> SET test redis
QUEUED
redis 127.0.0.1:6379> GET test
QUEUED
redis 127.0.0.1:6379> INCR visitors
QUEUED
redis 127.0.0.1:6379> EXEC

1) OK
2) "redis"
3) (integer) 1
```

**Các lệnh thường dùng**


| STT 	| Command 	| Ý nghĩa 	|
|-----	|---------	|----------------------------------------	|
| 1 	| MULTI 	| Đánh dấu bắt đầu khối lệnh transaction 	|
| 2 	| EXEC 	| Thực hiện khối lệnh 	|

### Bitmaps
* Bitmaps không phải là dạng dữ liệu thực tế, nhưng nó là tập hợp các bit định hướng hoạt động dựa trên kiểu String. Vì String là những blobs nhị phân có độ dài tối đa là 512MB nên phù hợp cho thiết lập 2^32 bit khác nhau. Bitmaps rất lý tưởng để tiết kiệm không gian khi lưu trữ thông tin dưới dạng các mảng bit

    ```bash
        > setbit key 0 1
        (integer) 0
        > setbit key 100 1
        (integer) 0
        > bitcount key
        (integer) 2
    ```

### HyperLogLogs
* Hyperloglog là một cấu trúc dữ liệu xác suất được sử dụng để đếm những phần tử riêng biệt (unique items - về mặt kỹ thuật điểu này được gọi là ước tính số lượng của một bộ). Thông thường việc đếm những unique items đòi hỏi phải sử dụng lượng bộ nhớ tương ứng với số lượng item muốn đếm bởi vì cần lưu trữ những element đã xuất hiện để tránh đếm chúng nhiều lần. Tuy nhiên, có một tập hơp các thuật toán cho phép giao dịch bộ nhớ với độ chính xác: kết thúc tại điểm ước tính có một lỗi tiêu chuẩn, trong trường hợp triển khai Redis nhỏ hơn 1%. Sự kí diệu của thuật toán này là không cần sử dụng lượng bộ nhớ tỉ lệ thuận với số mục được đềm, thay vào đó có thể sử dụng lượng bộ nhớ không đổi. 12k bytes trong trường hợp xấu nhất hoặc ít hơn nhiều nếu HiperLoglog đã thấy rất ít element.

- Bảng Function :

    Cú pháp	| Chức năng
    ---| ---
    PFADD key element [element ...]	 | Thêm môt phần tử cụ thể thuộc HyperLogLog.
    PFCOUNT key [key ...]  | Trả về gía trị lượng số (duy nhất) của đối tượng
    PFMERGE destkey sourcekey [sourcekey ...] | Merges N đối tượng HyperLogLogs khác nhau làm một.
- Ví dụ:

    ```bash
        > pfadd hll a b c d a c
        (integer) 1
        > pfcount hll
        (integer) 4
    ```

## Pub/Sub

Nắm được cách sử dụng pub/sub của Redis

https://redis.io/topics/pubsub

-   Pub - Publish: producer sẽ đẩy data vào một chanel.
-   Sub - Subscribe: consumer đăng ký nhận dữ liệu từ một chanel.

![](https://images.viblo.asia/c5051c43-10af-41ad-825e-b149a73f36c6.png)

Cái này giống như bạn xem Youtube. Bạn subscribe một channel. Khi một producer làm một video đẩy lên Youtube. Bạn sẽ nhận dữ liệu, tức xem video đó tại channel mà bạn đã subscribe. Khi bạn bè của bạn cũng subscribe channel đó, thì khi producer đẩy video lên, bạn và bạn bè của bạn cùng nhận được video để xem. Và tất nhiên, bạn có thể đăng ký nhiều channel.

**Demo**

Redis-cli hỗ trợ các command để Pub/Sub rất đơn giản:


-   SUB
```sh
$ redis-cli
127.0.0.1:6379> SUBSCRIBE channel [channel ...]
```

-   PUB
```sh
$ redis-cli                                                                                    
127.0.0.1:6379> PUBLISH channel message
```

Ta sẽ mở 2 console lên: 1 để `subscribe` và 1 để `publish`.

Console `subscribe`: ta sẽ subscribe channel tên là `test-console`:

```sh
127.0.0.1:6379> SUBSCRIBE test-console
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "test-console"
3) (integer) 1
```

Console `publish`: ta sẽ đẩy một vài message lên channel `test-console`:

```sh
127.0.0.1:6379> PUBLISH test-console "hello"
(integer) 0
127.0.0.1:6379> PUBLISH test-console "how are you?"
(integer) 0
```

Quay lại console subscribe ta sẽ nhận được message:

```sh
127.0.0.1:6379> SUBSCRIBE test-console
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "test-console"
3) (integer) 1
1) "message"
2) "test-console"
3) "hello"
1) "message"
2) "test-console"
3) "how are you?"
```


## Lock


Nắm được khái niệm cơ bản về lock 

https://en.wikipedia.org/wiki/Lock_(computer_science)

- Phân biệt Pessimistic locking và Optimistic locking

- Nắm được khái niệm distributed lock 

- Tìm hiểu thuật toán Redlock của Redis 

https://redis.io/topics/distlock


### Khái niệm cơ bản

- Trong khoa học máy tính, thuật ngữ **lock** hay **mutex** (từ _mutual exclusion (loại trừ tương hỗ)_) là một cơ chế đồng bộ để quản lý số lượng truy cập vào vùng tài nguyên cùng một thời điểm trong môi trường có nhiều _threads_ cùng thực thi. Một _lock_ được thiết kế để bắt buộc các _threads_ trên tuân theo chính sách điều khiển loại trừ tương hỗ.

- Trong **RDBMS** Locking là một cơ chế  ngăn chặn người dùng từ nhiều transactions khác nhau gây ra data conflicts. Locking một row giúp ngăn chặn các transactions khác thay đổi row đó cho đến khi transaction đang truy cập vào nó kết thúc. Trong đó có 2 chiến lược lock là: optimistic và pesimistic. 

### Optimistic và Pessimistic Locking

**Problem:** Giả sử 2 user A và B đều đọc chung dữ liệu Customer từ Database, sau đó cả 2 cùng thay đổi dữ liệu 1 bản ghi (customer x trong Database) và cùng cố gắng ghi dữ liệu (đã thay đổi) của mình vào Database. Vậy thì thay đổi nào sẽ được thực hiện: của A, B, cả 2 hay không ai cả.

**Solution:** Các Developer sẽ sử dụng locking để quản lý việc truy cập dữ liệu dùng chung. Vậy chúng ta nên dùng cơ chế locking nào để sử dụng, có 2 cơ chế locking cơ bản là Optimistic và Pessimistic.

![](http://labs.septeni-technology.jp/wp-content/uploads/2017/05/2a.jpg)
>https://labs.septeni-technology.jp/technote/optimistic-hay-pessimistic-locking/

#### Optimistic Locking

![](https://labs.septeni-technology.jp/wp-content/uploads/2017/05/OOL.png)

**Mục đích:** 
- Ngăn ngừa conflict giữa các transactions (nghiệp vụ) đồng thời bằng việc phát hiện ra conflict và thực hiện rollback transaction.
- Vấn đề tương tranh giữa các transaction thường xảy ra trong hệ thống có nhiều transactions đồng thời.
- Chúng ta không thể chỉ phụ thuộc vào việc quản lý database để đảm bảo các transaction nghiệp vụ sẽ ghi dữ liệu nhất quán được.
- Tính toàn vẹn của dữ liệu dễ ảnh hưởng bởi 2 session cùng hoạt động (update) trên các records, hoặc cũng có thể 1 session sửa dữ liệu và 1 session đọc dữ liệu không nhất quán cũng dễ xảy ra tương tự.
- Optimistic Locking giải quyết được problem trên bằng việc xác thực các thay đổi về việc commited trên từng session để không conflict đến session khác.

**Cách thức hoạt động:**
* Optimistic Offline Lock chứa 1 điều kiện validate. Tại 1 thời điểm, 1 session load dữ liệu của 1 record, session khác không được thay thế nó.
* Cài đặt phổ biến nhất là sử dụng version number cho với mỗi record trong hệ thống. Khi 1 record được load thì number đại diện cho version chứa được bởi session cùng với tất cả các trạng thái của session. Optimistic Offline Lock sẽ quan tâm đến việc so sánh dữ liệu number version lưu trong session data và current session trong record data. Nếu 2 giá trị number version bằng nhau tức việc verify thành công thì tất cả các thay đổi, bao gồm cả việc tăng version sẽ được committed.
* Đối với Database RDBMS, 1 câu lệnh SQL có thể thực hiện lock và update dữ liệu record. Transaction nghiệp vụ sẽ kiểm tra giá trị row_count trả về bởi SQL execution. Nếu row_count = 1 tức là cập nhật thành công, row_count = 0 tức là record đã bị changed hoặc deleted. Với row_count = 0, transaction nghiệp vụ bắt buộc phải thực hiện rollback lại system transaction để ngăn ngừa các thay đổi tác động vào record data.
* Ngoài thông tin version number của mỗi record, thông tin lưu trữ còn có thêm như user thực hiện modified record cuối cùng hoặc timestamp thời gian thay đổi.
* Có thể sử dụng câu điều kiện update vào tất cả các trường trong row: 

```sql
UPDATE Customer SET ..., version = (session’s copy of version + 1) 
WHERE id=? and version= session’s copy of version
```


#### Pessimistic Locking

![](https://labs.septeni-technology.jp/wp-content/uploads/2017/05/POL.png)

**Mục đích:**
- Với cách tiếp cận Optimistic Locking không giải quyết triệt để được với các trường hợp người dùng truy cập cùng một dữ liệu trong một transaction (1 transaction sẽ commit thành công và 1 transaction sẽ failed => rollback).
- Bởi vì sự phát hiện conflict xảy ra ở giai đoạn cuối transaction, do đó dữ liệu đã xử lý của transaction failed sẽ là lãng phí ?
- Pessimistic Locking đã ngăn ngừa việc conflict giữa chúng với nhau bằng cách khi thực hiện transaction sẽ lock dữ liệu trước khi sử dụng nó, trong thời gian transaction sử dụng dữ liệu đó sẽ đảm bảo chắc chắn việc không có xung đột nào xảy ra.

**Cách thức hoạt động:**

Để cài đặt được Pessimistic Locking cần làm:
- Xác định kiểu của lock mà bạn cần dùng
- Xây dựng lock manager
- Xác định đối tượng cho transaction để sử dụng locks.

Về lock type, chúng ta có 3 sự lựa chọn:
- Exclusive Write Lock: 
  - Chỉ cho phép 1 transaction được thực thi việc ghi dữ liệu.
  - Nó sẽ tránh được conflict bởi không cho phép 2 transactions nghiệp vụ nào được thay đổi cùng 1 dữ liệu đồng thời.
- Exclusive Read Lock: 
  - Chỉ có phép 1 transaction được thực thi đọc dữ liệu. 
  - Hai transactions sẽ không được đọc dữ liệu đồng thời
- Exclusive Read and Write Lock: 
  - Một record không thể bị thực hiện write-lock khi 1 transaction khác đang sở hữu read lock trên nó và ngược lại.
  - Concurrent read locks được chấp nhận. 
  - Tồn tại 1 single read lock ngăn ngừa business transaction từ việc sửa dữ liệu, nó sẽ không ảnh hưởng gì trong việc cho phép các sessions khác cùng đọc.

- Xây dựng lock manager: 
  - Công việc của Lock Manager là grant hoặc deny bất kỳ request nào bởi transaction nghiệp vụ cho việc thực thi hoặc release 1 lock. 
  - Để làm công việc đó, Lock Manager cần biết rõ những gì sẽ bị lock như là ý định của người lock.
  - Session và business transaction gần tương đương và có thể thay thế.
  - Lock Manager không nên chứa nhiều hơn 1 table quản lý các lock của owner. Đơn giản nhất là 1 in-memory hash table hoặc 1 database table.
  - Các transaction chỉ nên tương tác với lock manager và không được tương tác với lock object.

Chúng ta thường lock các object hoặc record, nhưng thật ra thứ cần lock thực sự là ID hoặc Primary Key (thứ để xác định tìm ra object). Nó cho phép chúng ta chứa lock trước khi load chúng.

Đối với Database RDBMS, ví dụ như MySQL có hỗ trợ 2 cơ chế lock là:
* Shared Lock Statement: LOCK IN SHARED MODE. Ví dụ: Có 2 bảng PARENT và CHILD, khi transaction thực hiện insert dữ liệu vào bảng CHILD cần đảm bảo rằng dữ liệu parent_id phải tồn tại ở bảng PARENT tại thời điểm đó.

    ```sql
    SELECT * FROM parent WHERE NAME = 'Jones' LOCK IN SHARE MODE;
    ```

Sau khi LOCK IN SHARE MODE, câu query sẽ trả về giá trị Jones và transaction có thể an toàn thực hiện insert dữ liệu vào bảng CHILD. Trong thời điểm đó các transaction khác thực hiện UPDATE, DELETE lên row chứa giá trị Jones sẽ phải chờ transaction ban đầu hoàn thành.
* Exclusive Lock Statement: FOR UPDATE. Cách giải quyết trên sẽ gặp phải vấn đề nếu 2 transaction cùng thực hiện đọc bảng PARENT với row Jones, và đều đọc được dữ liệu sau đó insert sẽ bị duplicate giá trị. Cách khắc phục triệt để là sử dụng SELECT FOR UPDATE:

    ```sql
    SELECT * FROM parent WHERE NAME = 'Jones' FOR UPDATE;
    ```

Khi thực hiện FOR UPDATE, transaction khác sẽ không tìm thấy dữ liệu từ bảng parent với row có name là Jones.


#### Kết luận

<p align="center">
        <img src="https://i1.wp.com/69.89.31.106/~maddukur/wp-content/uploads/2017/11/PesVsOpt.jpg?resize=525%2C328"/>
</p>

Chúng ta sẽ sử dụng mỗi cơ chế locking vào mỗi nghiệp vụ khác nhau:
* Optimistic Locking sử dụng phù hợp trong các trường hợp có nghiệp vụ xác suất conflict giữa 2 transaction là thấp. Nhược điểm của Optimistic Offline Locking là chỉ verify trên các câu lệnh UPDATE và DELETE, vẫn có thể gây ra inconsistent khi read dữ liệu.
* Pessimistic Locking sử dụng phù hợp trong các nghiệp vụ có khả năng xảy ra conflict cao. Nếu bạn sử dụng Pessimistic Lock, bạn nên cân nhắc đến việc xử lý timeout cho các long transaction để tránh deadlock.



### Distributed lock 
* Distributed lock được sử dụng để chia sẻ tài nguyên theo cách loại trừ lẫn nhau. Tức là tại một thời điểm, chỉ có một đối tượng kiểm soát được tài nguyên.
* Distributed lock là một cách căn bản hữu ích trong các môi trường mà có nhiều tiến trình khác nhau phải hoạt động với các tài nguyên được chia sẻ độc quyền


### Thuật toán Redlock của Redis
* Redlock là thuật toán thích hợp để cài đặt Distributed Lock Manager.
* Safety and Liveness guarantees
    * Safety property: Mutual Exclution. Tại bất kỳ một thời điểm, chỉ có 1 client có thể giữ lock.
    * Liveness property A: Deadlocks free. Cuối cùng, luôn có thể thu được lock, ngay cả khi nó đã bị giữ bởi một client khác bị crash (time-out).
    * Liveness property B: Failt Tolerance. Khi nào phần lớn Redis nodes còn hoạt động, client có khả năng acquire và release lock.

* Cách đơn giản nhất để Redis lock tài nguyên là tạo một key K trong thực thể đó. Key K được tạo có thời gian sống giới hạn, sử dụng cơ chế Redis Expire. Vì thế, tài nguyên có thể được release bằng nhiều cách (khi hết thời gian sống của key K,..). Khi client muốn release tài nguyên, nó xóa key K. Có vẻ như cách này hoạt động ổn. Nhưng nó sẽ gặp sự cố khi có tình huống:
    * Client A giữ lock tài nguyên T ở master.
    * Master bị crash trước khi key K được ghi xuống slave.
    * Slave được đưa lên làm master (không có key K).
    * Client B giữ lock tài nguyên T giống Client A.

    => Tình huống trên đã vi phạm cơ chế an toàn (Safety Violation).

* Thuật toán Redlock
    * Thay vì chỉ lock trên master giữ tài nguyên, ta sẽ lock trên tất cả các master.
    * Lấy thời gian hiện tại T0 theo miliseconds.
    * Thử lock trên tất cả các instance với cùng giá trị key và random_value. Trong suốt quá trình này, client sử dụng time-out để tránh liên lạc quá lâu với những node không hoạt động và chuyển sang node tiếp theo.
    * Client tính thời gian trôi qua để thu giữ lock bằng cách trừ thời gian hiện tại với thời gian T0 ở trên. Chỉ khi client có khả năng lock phần lớn các instance (ít nhất 3) và tổng thời gian trôi qua để thu giữ lock nhỏ hơn thời gian lock có hiệu lực thì lock đó coi như đã được giữ.
    * Nếu lock đã được nhận, thời gian hiệu lực thực sự của nó chính là thời gian hiệu lực khởi tạo ban đầu trừ đi thời gian trôi qua trong lúc tạo lock, như đã được tính trong bước trên.
    * Nếu client thất bại khi thu giữ lock, nó unlock trên tất cả các instance.