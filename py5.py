#爬取微博
import requests
import re
import os#创建文件夹
import csv
import time

def picwrite(pagei,no,picr,zutu=False,q=0):#爬原图
    if not os.path.exists(picpath):  # 判断当前根目录是否存在
        os.mkdir(picpath)  # 创建根目录
    if zutu==True and q!=0:
        with open(picpath + '{}_{}_{}.jpg'.format(pagei, no,q), 'wb') as jpg:
            jpg.write(picr.content)
            print(pagei, no, q,".jpg:文件保存成功")
    else:
        with open(picpath + '{}_{}.jpg'.format(pagei, no), 'wb') as jpg:
            jpg.write(picr.content)
            print(pagei, no, ".jpg:文件保存成功")


#https://weibo.cn/3176010690/info
picpath='C://Users//wzw//PycharmProjects//pc1//'
userid='3937348351'#用户id
url='https://weibo.cn/u/'+userid+'?page='
urlori='https://weibo.cn/u/'+userid+'?page=1'
header={
'cookie': 'ALF=1572843377; SCF=ArCCM07qmWH813M_lwt6qtKO7KGDNED7exp5C7QrWWLxA9WFp1EtUEXaIAJzAy4SylSGfwvaLER2AUcRiafZBhc.; SUB=_2A25wnFdpDeRhGeFP6FQW8C7OzjuIHXVQf3khrDV6PUJbktAKLVXzkW1NQTONj3YUDTA9HnlT_OA-7wqfNpoO4h-e; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWjlwP0bsD2qDe2MzErvok5JpX5K-hUgL.FoMpe0qNeh5ESKM2dJLoI0YLxK-L1K5L1hnLxKqL1-eL1hnLxK-LBoMLBoBLxK-LBoMLBK-LxKBLBonL1-2LxK-LBKBLBKMLxK-LB-BLBKqt; SUHB=0M2FLbwnaHZkEk; SSOLoginState=1570252601; MLOGIN=1; _T_WM=73780338213',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

r=requests.get(urlori,headers=header)
pagewz=re.search('1/(\d+)页',r.text)
username=re.search('class="ctt">(.*?)<img',r.text)
usernamestr=str(username.group(1))
picpath=picpath+usernamestr+'//'
page=int(pagewz.group(1))#页数
picurl='https://weibo.cn/mblog/oripic'
zutuurl='https://weibo.cn/mblog/picAll'
for i in range(1,page):
    newurl=url+str(i)
    r=requests.get(newurl,headers=header)
    time.sleep(0.1)
    zutus=re.findall('"https://weibo.cn/mblog/picAll(.*?)">组图',r.text)

    q=1
    j=1

    for zutu in zutus:
        zutur=requests.get(zutuurl+zutu,headers=header)
        pics = re.findall('"/mblog/oripic?(.*?)">原图</a>', zutur.text)
        for pic in pics:  # 爬取图片
            pic=re.sub('amp;','',pic)
            picr = requests.get(picurl + pic, headers=header)
            picwrite(i, j, picr,zutu=True,q=q)
            q += 1
            time.sleep(0.1)


    pics=re.findall('"https://weibo.cn/mblog/oripic(.*?)">原图</a>',r.text)
    for pic in pics:#爬取图片
        pic=re.sub('amp;','',pic)
        picr=requests.get(picurl+pic,headers=header)
        picwrite(i, j,picr)
        j += 1
        time.sleep(0.1)
