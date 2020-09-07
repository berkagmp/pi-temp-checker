# Register temp to system
```
sudo cp ./temp.sh /bin/temp
```
# DB Table
```
CREATE TABLE `temp` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cpu` float NOT NULL,
  `gpu` float NOT NULL,
  `time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
)
```
# Crontab

## Every 5 minites 

```
*/5 * * * * {Path}/python3 {Path}/temp.py >> {Path}/log/cron.log 2>&1
```