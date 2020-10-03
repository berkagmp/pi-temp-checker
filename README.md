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