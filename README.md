主要由Flask+Mysql+bootstrap搭建的爬虫数据查询应用

# Usage

1.在db.py配置好数据库连接

```
try:
    db = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="rootroot",database="tieba")
    cursor = db.cursor()
except Exception as e:
    print("[!]数据库连接失败,请检查数据库是否开启或者密码账号是否正确,或是tieba数据库是否创建")
    sys.exit(1)
```

2.启动go.py开始爬取

安装所需的模块

```
python -m pip install -r req.txt
```

```
usage: go.py [-h] -n NAME [-s START] -e END [-c COOKIE]

BaiduTieba-url-ip-title

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  贴吧名 eg:钓鱼吧需要输入钓鱼 不需要最后的'吧'字
  -s START, --start START
                        从这个吧的主页的第几页开始，默认为第一页
  -e END, --end END     结束页
  -c COOKIE, --cookie COOKIE
                        输入cookie，注意不要出现特殊字符，如一些url编码字符，用单引号包裹，默认从cook.txt读取
```

eg: 爬取钓鱼吧前3页的数据

```
python go.py -n 钓鱼 -s 1 -e 3
```

3.启动本地web服务查看数据

```
python app.py
```

