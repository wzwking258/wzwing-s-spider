# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
from lxml import etree
import mysql.connector
import sys
import json

mydb = mysql.connector.connect(#数据库初始化
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="pppppppp", # 数据库密码
  charset='utf8mb4'
)

#创建数据表
mycursor = mydb.cursor()#获取游标
mycursor.execute("CREATE DATABASE IF NOT EXISTS tiebapc3 DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;")
mycursor.execute("use tiebapc3;")
mycursor.execute("CREATE TABLE IF NOT EXISTS ties(`id` INT UNSIGNED AUTO_INCREMENT not null unique,`title` VARCHAR(200),`user_nickname` VARCHAR(70) NOT NULL,`user_nicknameCHN` VARCHAR(70),`user_oriname` VARCHAR(70),`submit_data` date,`submit_time` time,`last_cmd_date` date,`last_cmd_time` time,`cmd_num` int unsigned,`content` text,`tie_url` varchar(200) not null,PRIMARY KEY ( `tie_url` ))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  COLLATE=utf8mb4_unicode_ci;")

mycursor.execute("CREATE TABLE IF NOT EXISTS huifus(`title` VARCHAR(200),`user_nickname` VARCHAR(70),`user_nicknameCHN` VARCHAR(70),`user_oriname` VARCHAR(70),`commands` text,`lo` int not null,`cmd_time` datetime,`tie_url` varchar(200) not null,PRIMARY KEY ( `tie_url`,`lo` ))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")

tiebaname='steam'#贴吧名
url='https://tieba.baidu.com'
url1='https://tieba.baidu.com/f?kw=%E7%A5%9E%E5%A5%88%E5%B7%9D%E5%86%B2%E6%B5%AA%E9%87%8C'
webheaders={'Cookie': 'BAIDUID=E0DABE92EFA10C7A355FACD5EA10EF0D:FG=1; BIDUPSID=E0DABE92EFA10C7A355FACD5EA10EF0D; PSTM=1570104819; TIEBA_USERTYPE=151fb0a2bced42228d3e339d; bdshare_firstime=1570115080653; TIEBAUID=cb23caae14130a0d384a57f1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1463_21094_29568_29220; BDSFRCVID=uJFsJeCCxG3eSK5wdDguWev36vszyUfHdDX-3J; H_BDCLCKID_SF=JJkO_D_atKvjDbTnMITHh-F-5fIX5-RLf5TZKtOF5lOTJh0RbqbvjJ-OQMJtL-QqtbcqQ-cXQRQ1ehbyqjbke4tX-NFJq6DtJf5; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1574046678,1574482431,1574513281; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1574513281; delPer=0; PSINO=7',
'Host': 'tieba.baidu.com',
'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'}

for i in range(1,100000000):#第一页
    i=i%10
    if i%10==0:
        print('等待中………………600s')
        time.sleep(600)
    print('等待中………………10s')
    time.sleep(10)
    webparams = {'kw': tiebaname, 'ie': 'utf-8', 'pn': i * 50}
    r = requests.get(url+'/f',params=webparams,headers=webheaders)
    print(r.status_code)
    soup=BeautifulSoup(r.text,'lxml')
    fullties=soup.find_all(name='li',attrs={'class':'j_thread_list clearfix'})
    for fulltie in fullties:

        title = ''
        user_nickname = ''  # ties的字段
        user_nicknameCHN = ''
        user_oriname = ''
        submit_data ='1111-11-11'#默认时间，因为时间不能为空
        submit_time = ''
        last_cmd_time = ''
        last_cmd_date='1111-11-11'#默认时间，因为时间不能为空
        cmd_num = ''
        content = ''
        tie_url = ''

        soup2=BeautifulSoup(str(fulltie.div),'lxml')#前面查找的是str字符串！后面的不可缺失！
        title=soup2.find(name='a',attrs={'class':"j_th_tit"})
        detail=soup2.find(name='div',attrs={'class':'threadlist_abs threadlist_abs_onlyline'})
        auther=soup2.find(name='span',attrs={'class':"tb_icon_author"})
        time1=soup2.find(name='span',attrs={'class':'pull-right is_show_create_time'})
        time2 = soup2.find(name='span', attrs={'title':"最后回复时间"})
        autherid =soup2.find(name='a', attrs={'class':"frs-author-name j_user_card"})
        if autherid==None:
            autherid = soup2.find(name='a', attrs={'class': "frs-author-name sign_highlight j_user_card vip_red"})
        if autherid == None:
            autherid = soup2.find(name='a', attrs={'class': "frs-author-name sign_highlight j_user_card"})
        if autherid == None:
            autherid = soup2.find(name='a', attrs={'class': "frs-author-name j_user_card vip_red"})
        commendnum=soup2.find(name='span', attrs={'title':"回复"})
        imgurls=soup2.find_all(name='img', attrs={'class':"threadlist_pic j_m_pic"})

        titlestr=title.get_text('title').strip()#贴子标题
        detailstr=detail.text.strip()#贴子的详细内容
        autherstr=re.search('"主题作者:(.*?)"',str(auther))#贴子作者的用户名
        autheridstr=' '
        if autherid!=None:
            autheridstr=re.search('"un":"(.*?)",',autherid.attrs['data-field'])#贴子作者的id
        timefastr=time1.text.strip()#贴子的发贴时间
        timehuistr = time2.text.strip()#贴子的最后回复时间
        tieurl=str(url+title.attrs['href'])#贴子的url
        commendsnum=commendnum.text#贴子的评论数
        unautheridstr= re.search('"author_nickname":"(.*?)",',fulltie.attrs['data-field'])
        unautheridstr2=''
        if unautheridstr != None:
            unautheridstr2=unautheridstr.group(1)
        imgs=[]
        for imgurl in imgurls:
            imgs.append(imgurl.attrs['bpic'])
        autheridstrz=' '
        if autheridstr!=None:
            autheridstrz=str(autheridstr.group(1)).encode('utf-8').decode('unicode_escape')

        #print(imgs)
        print('贴子:'+titlestr+' 楼主 '+autherstr.group(1)+' '+'('+unautheridstr2+')'+autheridstrz+' 创建时间 ：'+timefastr +" 最后回复时间 "+timehuistr+' 回复数:'+commendsnum+'\n'+'内容:'+detailstr+'\n'+tieurl)
        print('\n')

        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
        strtime = re.sub('\s|:', '_', localtime)  # 现在的时间
        autherstrssk=autherstr.group(1)

        title = titlestr
        user_nickname = unautheridstr2  # ties的字段
        user_nicknameCHN =autherstrssk
        user_oriname = autheridstrz
        if '-' in timefastr:
            submit_data = '2019-'+timefastr
        elif ':' in timefastr:
            submit_time=timehuistr+':00'

        if '-' in timehuistr:
            last_cmd_date = '2019-'+timehuistr
        elif ':' in timehuistr:
            last_cmd_time = timehuistr+':00'
        cmd_num = commendsnum
        content = detailstr
        tie_url = tieurl
        insertgcmd='insert ignore into ties (title,user_nickname,user_nicknameCHN,user_oriname,submit_data,submit_time,last_cmd_date,last_cmd_time,cmd_num,content,tie_url) values '
        repcmd='replace into ties (title,user_nickname,user_nicknameCHN,user_oriname,submit_data,submit_time,last_cmd_date,last_cmd_time,cmd_num,content,tie_url) values '
        val=f'(\'{title}\',\'{user_nickname}\',\'{user_nicknameCHN}\',\'{user_oriname}\',\'{submit_data}\',\'{submit_time}\',\'{last_cmd_date}\',\'{last_cmd_time}\',{cmd_num},\'{content}\',\'{tie_url}\');'
        mycursor.execute(repcmd+val)
        mydb.commit()    # 数据表内容有更新，必须使用到该语句

        tier=requests.get(tieurl, headers=webheaders)
        souptie=BeautifulSoup(tier.text,'lxml')
        ye=souptie.find(name='li',attrs={'class':'l_reply_num'})
        if ye!=None:
            print(ye.span.next_sibling.next_sibling.text)#下一个兄弟节点的值
            yeshu=int(ye.span.next_sibling.next_sibling.text) #页数
        else:
            yeshu=1
        for j in range(1,yeshu+1):
            print('等待中………………5s')
            time.sleep(5)
            fullcommends=souptie.find_all(name='div',attrs={'class':'l_post l_post_bright j_l_post clearfix'})
            for fullcommend in fullcommends:
                title = ''
                user_nickname = ''  # ties的字段
                user_nicknameCHN = ''
                user_oriname = ''
                tie_url = ''
                commands = ''
                lo =0
                cmd_time = ''
                tiesoup2 = BeautifulSoup(str(fullcommend), 'lxml')
                try:
                    cmdauthor=tiesoup2.find(name='a', attrs={'class':"p_author_name j_user_card"})
                    if cmdauthor==None:
                        cmdauthor=tiesoup2.find(name='a', attrs={'class':"p_author_name j_user_card vip_red"})
                    if cmdauthor == None:
                        cmdauthor = tiesoup2.find(name='a', attrs={'class': "p_author_name sign_highlight j_user_card"})
                    if cmdauthor == None:
                        cmdauthor = tiesoup2.find(name='a', attrs={'class': "p_author_name sign_highlight j_user_card vip_red"})
                    cmd = tiesoup2.find(name='div', attrs={'class': "d_post_content j_d_post_content"})
                    cmdtime_no=tiesoup2.find(name='div', attrs={'class': "post-tail-wrap"})
                    if cmdauthor != None:
                        cmdautherid=re.search('"un":"(.*?)",',cmdauthor.attrs['data-field'])#贴子作者的id
                    cmdauthorstr=cmdauthor.text.strip()
                    cmdauthorstr2 = re.search('"user_nickname":"(.*?)"},"content":',fullcommend.attrs['data-field'])
                    cmdauthorstr2s=' '
                    if cmdauthorstr2!=None:
                        cmdauthorstr2s = str(cmdauthorstr2.group(1)).encode('unicode_escape','ignore').decode('unicode_escape')
                        #考虑是某些字符无法解码为utf-8的编码格式，把dataframe(meta)的元素，在编码过程中，先把无法转化为utf-8格式的字符‘ignore’掉，再进行解码。
                    cmdstr=cmd.text.strip()
                    cmdnostr=re.search('(\d*)楼',str(cmdtime_no))
                    cmdtimestr = re.search('(\d*?-\d*?-\d*?\s\d*?:\d*)', str(cmdtime_no))

                    cmdautheridstr=' '
                    if cmdautherid!= None:
                        cmdautheridstr = str(cmdautherid.group(1)).encode('utf-8').decode('unicode_escape')
                    print(cmdauthorstr,'('+cmdauthorstr2s+')',cmdautheridstr,cmdstr,cmdnostr.group(1)+'楼',cmdtimestr.group())

                    user_nickname=cmdauthorstr2s
                    user_nicknameCHN=cmdauthorstr
                    user_oriname=cmdautheridstr
                    commands=cmdstr
                    lo=int(cmdnostr.group(1))
                    cmd_time=cmdtimestr.group()+':00'
                    tie_url=tieurl
                    title=titlestr
                    insertgcmdh = 'insert ignore into huifus (user_nickname,user_nicknameCHN,user_oriname,commands,lo,cmd_time,tie_url,title) values '
                    repcmdh = 'replace into huifus (user_nickname,user_nicknameCHN,user_oriname,commands,lo,cmd_time,tie_url,title) values '
                    valh = f'(\'{user_nickname}\',\'{user_nicknameCHN}\',\'{user_oriname}\',\'{commands}\',{lo},\'{cmd_time}\',\'{tie_url}\',\'{title}\');'
                    mycursor.execute(insertgcmdh + valh)
                    mydb.commit()  # 数据表内容有更新，必须使用到该语句
                    #楼中楼的和回复
                except:
                    print('错误？！1')

            try:
                print(tier.status_code)#tier已经request请求了
                soupl = BeautifulSoup(tier.text, 'lxml')
                tieid = re.search('https://tieba.baidu.com/p/(\d*)$', tieurl)#tieurl是当前贴的url
                fidtag = soupl.find(name='div', attrs={'class': 'wrap1'}).find(name='script',attrs={'type': 'text/javascript'})
                fid = re.search('forum_id: "(\d*?)",', str(fidtag))
                tid = tieid.group(1)
                fid = fid.group(1)
                jstr = str(j)
                urlpl = 'https://tieba.baidu.com/p/totalComment?t=146447' + '&tid=' + tid + '&fid=' + fid + '&pn=' + jstr + '&see_lz=0'

                lzlr = requests.get(urlpl, headers=webheaders)
                if lzlr==None:
                    break
                j = json.loads(lzlr.text)  # str转化为json文件
                   # print(j)
                if type(j['data']['comment_list'])!=dict:
                    break
                print(tier.status_code)  # tier已经request请求了
                ks = j['data']['comment_list'].keys()  # 类似集合的元素
                k1 = list(ks)[0]
                keys = j['data']['comment_list'][k1]['comment_info'][0].keys()
                keysl = list(keys)
                lolzl=0
                for k in j['data']['comment_list'].keys():
                    sz = len(j['data']['comment_list'][k]['comment_info'])
                    for i in range(sz):
                        for k2 in keysl:
                            if k2 in j['data']['comment_list'][k]['comment_info'][i].keys():
                                if k2 == 'username':
                                    user_oriname = j['data']['comment_list'][k]['comment_info'][i][k2]
                                elif k2 == 'content':
                                    commands = re.sub('<a href=""  onclick="Stats.sendRequest.*?class="at">|</a>', '',
                                                          j['data']['comment_list'][k]['comment_info'][i][k2])
                                elif k2 == 'now_time':
                                    localtime = time.gmtime(j['data']['comment_list'][k]['comment_info'][i][k2])
                                    cmd_date = str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(
                                        localtime.tm_mday)
                                    cmd_time = str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(
                                        localtime.tm_sec)
                        lolzl=lolzl-1
                        cmd_time=cmd_date+' '+cmd_time
                        insertlzlcmd = 'insert ignore into huifus (user_oriname,lo,commands,cmd_time,tie_url) values '
                        vallzl = f'(\'{user_oriname}\',{lolzl},\'{commands}\',\'{cmd_time}\',\'{tie_url}\');'
                        mycursor.execute(insertlzlcmd + vallzl)
                        mydb.commit()  # 数据表内容有更新，必须使用到该语句
                        print(user_oriname,commands,end=' ')
                        print(cmd_time)
                        print()
            except:
                print('错误！？2')
            tier = requests.get(tieurl+'?pn='+str(i+1), headers=webheaders)
            souptie = BeautifulSoup(tier.text, 'lxml')
