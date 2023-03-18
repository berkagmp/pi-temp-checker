# Register temp to system
```
sudo cp ./temp.sh /bin/temp
```

# MySQL Table
```
CREATE TABLE `temp` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cpu` float NOT NULL,
  `gpu` float NOT NULL,
  `time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
)
```
```
CREATE TABLE `soap_room` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `temp` double(8,2) NOT NULL,
  `humidity` double(8,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
);
```
```
CREATE TABLE `email_queue` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `recipient` varchar(100) NOT NULL,
  `cc` varchar(100) DEFAULT NULL,
  `subject` varchar(200) NOT NULL,
  `body` varchar(500) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
);
```

# MongoDB
## pymongo for MongoDB 2.4
```
pip3 install pymongo==3.4.0
```

# DHT11 Compile
```
gcc -o dht dht.c -lwiringPi -lwiringPiDev
sudo cp ./dht /bin/dht
```

# Crontab

## Every 5 minites 

```
*/5 * * * * {Path}/python3 {Path}/temp.py >> {Path}/log/cron.log 2>&1
```
