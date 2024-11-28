from flask import Flask,render_template,request
from db import *

app = Flask(__name__)

ipWhere = ['查询全部','北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','中国香港','中国澳门','中国台湾','其他']

def getBa():
    Ba = []
    allBa = getAllT()
    for row in allBa:
        for co in row:
            Ba.append(co)
    return Ba

def getPageData(Tname,page):
    Column = []
    allRes = searchSome(Tname,page)
    for row in allRes:
        Column.append(row)
    return Column

def getNameDict(Tname):
    nameDict = ipCount(Tname)
    return nameDict
    
@app.route("/",methods=['get','post'])
def index():
    ip = ""
    Tname = ""
    allPage = 0
    currentPage = 1
    Ba = getBa()
    Column = []
    nameDict = {}
    if(request.args.get('query')):
        Tname = request.args.get('query')

    if(request.args.get('page')):
        currentPage = request.args.get('page')

    if(request.args.get('query') and request.args.get('ip') =='查询全部'):
        allPage = allCount(Tname)
        ip = request.args.get('ip')
        nameDict = getNameDict(Tname)
        Column = getPageData(Tname,currentPage)

    if(request.args.get('ip') and request.args.get('ip')!='查询全部'):
        ip = request.args.get('ip')
        allPage = ipCount1(Tname,ip)
        sbyip = searchIP(Tname,ip,currentPage)
        for row in sbyip:
            Column.append(row)
        if(request.args.get('ip')=="其他"):
            allPage = elseCount(Tname)
            elser = searchElse(Tname,currentPage)
            for row in elser:
                Column.append(row)

    return render_template("index.html",Ba=Ba,Column=Column,ipWhere=ipWhere,nameDict=nameDict,allPage=allPage,currentPage=currentPage,Tname=Tname,ip=ip)

@app.route("/count",methods=['get','post'])
def count():
    nameDict = ipCount(request.args.get('query'))
    Tname = request.args.get('query')
    return render_template("count.html",nameDict=nameDict,Tname=Tname)




if __name__ == "__main__":
    app.run(debug=True,host="127.0.0.1",port=23339)