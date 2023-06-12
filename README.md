## 资产梳理脚本

提取IP、Domain、URL...

```
 ~/assetParser/ python assetParser.py -h
usage: assetParser.py [-h] -f RAWINPUTFILE

options:
  -h, --help       show this help message and exit
  -f RAWINPUTFILE  Raw Input File
 ~/assetParser/ 
 ~/assetParser/ python assetParser.py -f test/tmp.txt
invalid IP: 222.190.342.193

extract  7395  IPs     to test/tmp_ip.txt

extract   515  DOMAINs to test/tmp_domain.txt

extract  1555  URLs    to test/tmp_url.txt
```



### IP格式

- \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}
- \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}
- \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}
- \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}


### domain格式
- [\w\.-]+\.(cn|com|net|top|io|org|info|vip|xyz)
  

### url格式
- https?://[\w\.-]+(:\d+)?(/\S*)?
