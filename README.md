Cài đặt SNORT, BARNYARDv2 và BASE
Bước chuẩn bị
========
- Cài đặt Ubuntu 22.04
- Update sources
- Cài đặt thêm các gói phát triển phần mềm

1) sudo apt-get update
2) sudo apt-get install net-tools
3) sudo apt-get install build-essential

Cài đặt SNORT
========
1) sudo apt-get install snort
2) soạn thảo 1 luật đơn giản phát hiện khi có máy nào ping vào máy chúng ta
sudo nano /etc/snort/rules/local.rules

alert icmp any any -> $HOME_NET any (msg:"ICMP test detected"; GID:1;
sid:10000001; rev:001; classtype:icmp-event;)

3) xem giao diện card mạng, có thể là eth0, eno0, enss3, etc.
ifconfig
Ví dụ giao diện mạng là enss3.

4) Mở snort để phát hiện các dấu hiệu bất thường trên mạng tại giao diện enss3, hiển thị các cảnh báo lên console
sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i enss3

5) Tắt luật "SCAN UPnP service discover attempt"
sudo grep "SCAN UPnP service discover attempt" /etc/snort/rules/*
sudo nano /etc/snort/rules/scan.rules
chú thích bằng dấu # trước luật "SCAN UPnP service discover attempt"

6) Thực thi lại snort để phát hiện các dấu hiệu bất thường trên mạng tại giao diện enss3, hiển thị các cảnh báo lên console
sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i enss3

7) Mở terminal trên 1 máy, thực hiện lên ping đến máy chúng ta có địa chỉ ip, chẳng hạn là 192.168.1.7
ping 192.168.1.7
Quan sát xem trên máy chúng ta có hiển thị "ICMP test detected"

Cài đặt LAMP
========

1) Cài đặt apache
sudo apt install apache2 -y

2) Cài đặt mysql server
sudo apt install mysql-server libmysqlclient-dev mysql-client autoconf libtool -y
sudo mysql_secure_installation

cấu hình mysql:
- chế độ security với (VALIDATE PASSWORD PLUGIN)
- mức độ security
LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary file
- Đặt mật khẩu cho root
- Xoá guest user
- Xoá CSDL test

3) Cài đặt PHP 5.6 (do BASE chỉ hoạt động trên PHP < 5.7)
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update -y
sudo apt-get install -y libapache2-mod-php5.6 php5.6 php5.6-common php5.6-gd php5.6-cli php5.6-xml php5.6-mysql
sudo apt-get install -y php-pear libphp-adodb

sudo apt-get install software-properties-common
sudo systemctl restart apache2

4) Kiểm tra LAMP
- Soạn thảo tập tin info.php như sau:
<?php
phpinfo();
?>

- Chép info.php vào thư mục web:
sudo cp info.php /var/www/html/

- Mở trình duyệt web: http://192.168.1.7/info.php
Quan sát xem các thành phần của LAMP có hoạt động đầy đủ không? Đặc biệt là php-mysql, php-pear, php-adodb.
 
Cài đặt BARNYARDv2
========

1) Cài đặt các gói phụ trợ cho xử lý các gói tin dạng pcap
sudo apt-get install libpcap-dev
sudo apt-get install libpcre3-dev
sudo apt-get install libdumbnet-dev
sudo apt-get install liblua5.2-dev
sudo apt-get install libnghttp2-dev
sudo ldconfig

2) Thay đổi cấu hình SNORT
a) Thay đổi /etc/snort/snort.conf
sudo vi /etc/snort/snort.conf

# Add after output unified2: filename merged.log, limit 128, nostamp, mpls_event_types, vlan_event_types
output unified2: filename snort.u2, limit 128

# Enable the local.rules file, and subsequent include files are commented out
include $RULE_PATH/local.rules

b) Tạo tập tin /etc/snort/sid-msg.map
sudo touch /etc/snort/sid-msg.map
sudo vi /etc/snort/sid-msg.map

1 || 10000001 || 001 || icmp-event || 0 || ICMP Test detected || url,tools.ietf.org/html/rfc792

c) Tắt firewall
sudo ufw disable

3) Download source và biên dịch
wget https://github.com/firnsy/barnyard2/archive/v2-1.13.tar.gz -O barnyard2-2-1.13.tar.gz

tar zxvf barnyard2-2-1.13.tar.gz
cd barnyard2-2-1.13
autoreconf -fvi -I ./
./configure --with-mysql --with-mysql-libraries=/usr/lib/x86_64-linux-gnu
sudo make & make install

4) Kiểm tra
barnyard2 -V

5) Cấu hình BARNYARDv2 kết nối với SNORT
sudo cp barnyard2-2-1.13/etc/barnyard2.conf /etc/snort/

sudo mkdir /var/log/barnyard2

sudo chown snort.snort /var/log/barnyard2

sudo touch /var/log/snort/barnyard2.waldo

sudo chown snort.snort /var/log/snort/barnyard2.waldo

6) Tạo CSDL hệ thống snort trong mysql
sudo mysql

mysql> create database snort;
mysql> use snort;
mysql> source barnyard2-2-1.13/schemas/create_mysql;
mysql> CREATE USER 'snort'@'localhost' IDENTIFIED BY '123456';
mysql> grant create, insert, select, delete, update on snort.* to 'snort'@'localhost';
mysql> exit;

7) Thay đổi tập tin cấu hình BARNYARDv2
sudo nano /etc/snort/barnyard2.conf

output database: log, mysql, user=snort password=123456 dbname=snort host=localhost sensor name=sensor01

sudo chmod 644 /etc/snort/barnyard2.conf

8) Khởi động mysql
service mysql start

9) Khởi động lại SNORT
sudo snort -q -u snort -g snort -c /etc/snort/snort.conf -i enss3

10) Mở BARNYARDv2 để kiểm tra
###Continuous processing mode, set barnyard2.waldo as bookmark
sudo barnyard2 -c /etc/snort/barnyard2.conf -d /var/log/snort -f snort.u2 -w /var/log/snort/barnyard2.waldo -g snort -u snort

- Quan sát xem khi có máy khác ping vào 192.168.1.7, trên barnyard có hiển thị thông điệp cảnh báo
 
- Có thể xem lại trong mysql

mysql -u snort -p -D snort -e "select count(*) from event"

Cài đặt ADOdb
========== 
1) Download source
wget https://sourceforge.net/projects/adodb/files/adodb-php5-only/adodb-520-for-php5/adodb-5.20.8.tar.gz

2) Cài đặt vào thư mục /var/www/html/adodb
sudo tar zxvf adodb-5.20.14.tar.gz -C /var/www/html
sudo mv /var/www/html/adodb5 /var/www/html/adodb

Cài đặt BASE
=========
1) Download source  
wget http://sourceforge.net/projects/secureideas/files/BASE/base-1.4.5/base-1.4.5.tar.gz

2) Cài đặt vào thư mục /var/www/html/base
sudo tar zxvf base-1.4.5.tar.gz -C /var/www/html
sudo mv /var/www/html/base-1.4.5 /var/www/html/base

3) Khởi động lại apache
sudo /etc/init.d/apache2 restart

4) Thay đổi cấu hình PHP
sudo nano /etc/php/5.6/apache2/php.ini

error_reporting = E_ALL & ~E_NOTICE

sudo /etc/init.d/apache2 restart

sudo chown -R root:root /var/www/html
sudo chmod 755 /var/www/html/adodb

5) Cấu hình cho BASE
Mở trình duyệt web gõ vào link: http://localhost/base/setup/index.php

Step 1: Select the language simplified_chinese and fill in the directory where ADOdb is located/var/www/html/adodb.

Step 2: Fill in the information in the database as previously configured (Archive database information may not be filled in).

Step 3: Fill in the administrative account: snort, password: 123456.

Step 4: Create a data table.

Step 5: Tip to copy the displayed information to / var/www/html/base/base_conf.php
