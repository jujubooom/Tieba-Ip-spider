import pymysql
import sys
try:
    db = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="rootroot",database="tieba")
    cursor = db.cursor()
except Exception as e:
    print("[!]数据库连接失败,请检查数据库是否开启或者密码账号是否正确,或是tieba数据库是否创建")
    sys.exit(1)

ipWhere = ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','中国香港','澳门','中国台湾','其他']
def createT(Tname):
    sql = f'''CREATE TABLE `{Tname}` (
  `url` varchar(255) NOT NULL DEFAULT '',
  `title` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;'''
    cursor.execute(sql)

def insertC(Tname,content):
    sql = f'''insert into {Tname}(url,title,ip) values('{content[0]}','{content[1]}','{content[2]}');'''
    try:
       cursor.execute(sql)
    except Exception as e:
        print("存在重复的url,此条不会重复存入数据库")

def deleteT(Tname):
    pass

def searchAll(Tname):
    sql = f'''select * from {Tname} order by 2'''
    cursor.execute(sql)
    return cursor.fetchall()

def searchSome(Tname,page):
    start = (int(page)-1) * 70
    end = 70
    sql = f'''select * from {Tname} order by 2 limit {start},{end}'''
    cursor.execute(sql)
    return cursor.fetchall()

def getAllT():
    sql = f'''show tables'''
    cursor.execute(sql)
    return cursor.fetchall()

def searchIP(Tname,ip,page):
    start = (int(page)-1) * 70
    end = 70
    sql = f'''select * from {Tname} where ip="{ip}" limit {start},{end}'''
    cursor.execute(sql)
    return cursor.fetchall()

def searchElse(Tname,page):
    start = (int(page)-1) * 70
    end = 70
    sql = f'''select * from {Tname} where ip NOT IN ( '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门', '台湾') limit {start},{end}'''
    cursor.execute(sql)
    return cursor.fetchall()

def isTexsit(Tname):
    flag = 0
    allT = getAllT()
    for row in allT:
        if Tname == row[0]:
            flag = 1
            break
    return flag
            
        
def ipCount(Tname):
    nameDict = {}
    for i in ipWhere:
        sql = f'''select count(ip) from {Tname} where ip="{i}"'''
        cursor.execute(sql)
        nameDict[i] = cursor.fetchone()[0]
    return nameDict

def allCount(Tname):
    sql = f'''select count(ip) from {Tname}'''
    cursor.execute(sql)
    return cursor.fetchone()[0]

def ipCount1(Tname,ip):
    sql = f'''select count(ip) from {Tname} where ip="{ip}"'''
    cursor.execute(sql)
    return cursor.fetchone()[0]

def elseCount(Tname):
    sql = f'''select count(ip) from {Tname} where ip NOT IN ( '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门', '台湾')'''
    cursor.execute(sql)
    return cursor.fetchone()[0]

    

    



