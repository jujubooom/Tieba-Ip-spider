import requests
import re
import time
import sys
from db import *
import argparse
import random
from multiprocessing.dummy import Pool
import multiprocessing
from myua import getUA



def ParseArgs():
    parser = argparse.ArgumentParser(description="BaiduTieba-url-ip-title")
    parser.add_argument("-n", "--name", type=str, help="贴吧名 eg:钓鱼吧需要输入钓鱼  不需要最后的'吧'字", required=True)
    parser.add_argument("-s", "--start", type=int, default=1, help="从这个吧的主页的第几页开始，默认为第一页", required=False)
    parser.add_argument("-e", "--end", type=int, help="结束页", required=True)
    parser.add_argument("-t", "--threads", type=int,default=5, help="线程数量,允许1-10,默认5", required=False)
    parser.add_argument("-c", "--cookie", type=str, help="输入cookie,注意不要出现特殊字符,如一些url编码字符,用单引号包裹,默认从cook.txt读取", required=False)
    return parser.parse_args()

args = ParseArgs()

if(args.threads>0 and args.threads<11):
    pass
else:
    print("线程仅允许1-10")
    sys.exit(1)

ip = []

if(args.cookie):
  header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Cookie' : args.cookie
}
else:
    with open("cookie.txt",'r') as f:
        header = {
    'User-Agent' : getUA(),
    'Cookie' : f.read()
}


#获取本页面中所有帖子的url
def get_page_url(page):
    pn = (page - 1)*50 #pn为页码控制参数没加一页pn就加50
    url = "https://tieba.baidu.com/f"
    param = {
    'ie' : 'utf-8',
    'kw' : args.name,  #吧名
    'pn' : pn
 }
    while(1):
        res = requests.get(url=url,params=param,headers=header)
        res.encoding = res.apparent_encoding
        if(re.findall(r'<title>百度安全验证</title>',res.text)):
            print("[!]该换cookie啦")
            print(f"[!]最后到第{page}页,做个人工验证,换完cookie再继续吧")
            sys.exit(1)
        #print(res.text)
        person_url = re.findall(r'/p/[0-9]*',res.text)
        #print(person_url)
        if(person_url!=[]):
            break
    return person_url

#请求帖子获取ip地址和标题
def get_info(url,page):
    info = []
    res = requests.get(url=url,headers=header)
    print(url)
    #有时候会被系统检测到需要换cookie
    if(re.findall(r'<script src="https://ppui-static-wap.cdn.bcebos.com/static/touch/js/mkdjump',res.text)):
        print("该换cookie啦")
        print(f"[!]最后到第{page}页,做个人工验证,换完cookie再继续吧")
        sys.exit(1)
    if(re.findall(r'已被吧务删除',res.text)):
        return '404'
    if(re.findall(r'当用户的帐号被屏蔽时，用户发布的贴子会被隐藏。',res.text)):
        return '404'
    ip = re.search(r"(?<=IP属地:)(\w+)",res.text)
    title = re.search(r"<title>(.*)</title>",res.text)
    if ip != None:
        ipp = ip.group()
    else:
        ipp = "未知IP"
    if title != None:
        titlee = title.groups()[0]
    else:
        titlee = "未知标题"
    info.append(ipp)
    info.append(titlee)
    return info


def spide_ip(Tname,start,end):
    url1 = []
    while(1):
        if(start > end):
            break
        url1 = get_page_url(start)
        #print(url1)
        #print(url1)
        url2 = ['https://tieba.baidu.com' + urlll for urlll in url1]

        def do(url):
            info = get_info(url,start)
            if(info != '404'):
                infos = [url,info[1],info[0]]
                #if single_ip == '广西' or single_ip == '海南':
                print(f"[+]{info[0]} : {url} : {info[1]}")
                insertC(Tname,infos)
                time.sleep(random.uniform(0.1,0.2)) 
        
        pool = Pool(args.threads)
        try:
          pool.map(do,url2)
        except multiprocessing.TimeoutError:
            print("Timeout occurred, terminating the program")
            pool.terminate()
            pool.join()
        url2 = []
        print(f"[+]第{start}页的所有帖子的IP保存完毕")   
        start += 1
    #print(url2)
    print("[+]done~~~")

if __name__ == "__main__":
    if(isTexsit(args.name)==0):
        createT(args.name)
    if(args.start):
        spide_ip(args.name,args.start,args.end)
    else:
        spide_ip(args.name,1,args.end)

    


         
    
    
















