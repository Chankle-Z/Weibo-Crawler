import requests
import parsel
import csv
import re
from urllib.parse import quote
import time

#伪装登录
headers={
'cookie': '',
'referer': '',
'user-agent': ''
}
key=input('请输入关键字：')
keyc=quote(key,'utf-8')
f =open(key+'.csv',mode='a',encoding='utf-8',newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(['name','time','content'])
count=1
for i in range(1,51):
    i=str(i)
    url='https://s.weibo.com/weibo?q='+keyc+'&page='+i
    responsequery=requests.get(url,headers=headers)
    html_data=responsequery.text
    patternuid = r'(?<=uid=).*(?=&mid)'
    patternmid = r'(?<=mid=).*(?=&pic_ids)'
    uids=re.findall(patternuid,html_data)
    mids=re.findall(patternmid,html_data)
    uids = uids[0:-1]
    mids = mids[0:-1]
    for uid, mid in zip(uids, mids):
        pattern = r'(?<=' + uid + '/).*(?=&?refer_flag=)'
        con = re.findall(pattern, html_data)
        con=con[1]
        con = con[0:9]
        url_main='https://weibo.com/ajax/statuses/show?id='+con
        response_main=requests.get(url_main,headers=headers)
        count=str(count)
        csv_writer.writerow('帖子' + count)
        count=int(count)
        count=count+1
        json_data_main = response_main.json()
        maincon = json_data_main['text_raw']
        maintime = json_data_main['created_at']
        mainname = json_data_main['user']['screen_name']
        csv_writer.writerow([mainname, maintime, maincon])
        urla='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='
        urlb='&is_show_bulletin=2&is_mix=0&count=10&uid='
        urlc='&fetch_level=0'
        urlcon=urla+mid+urlb+uid+urlc
        ##url_main = 'https://weibo.com/ajax/statuses/show?id=Mz1Yj8Q90'
        responsecon=requests.get(urlcon,headers=headers)
        ##response_main = requests.get(url_main, headers=headers)
        #获取数据
        #.text   .json()  .content
        json_data=responsecon.json()
        ##json_data_main = response_main.json()
        #解析数据
        #结构化数据解析 .json()  数据[]/{}  字典数据类型 方便接下来取值
        #非结构化数据解析 网页源代码 css/xpath/re
        #bs4,lxml,parsel(工具)
        datas=json_data['data']
        max_id=json_data['max_id']
        max_id1=str(max_id)
        ##maincon=json_data_main['text_raw']
        ##maintime=json_data_main['created_at']
        ##mainname=json_data_main['user']['screen_name']
        ##csv_writer.writerow([mainname,maintime,maincon])
        for data in datas[0:-1]:
            name=data['user']['screen_name']
            content = data['text_raw']
            time=data['created_at']
            print(name,time,content)
            csv_writer.writerow([name, time, content])
        while max_id1 != '0':
            url1='https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id='
            url2='&is_show_bulletin=2&is_mix=0&max_id='
            url3='&count=20&uid='
            url4='&fetch_level=0'
            urlt=url1 +mid+url2+ max_id1+url3+uid+url4
            response = requests.get(urlt, headers=headers)
            json_data = response.json()
            datas = json_data['data']
            max_id = json_data['max_id']
            max_id1=str(max_id)
            for data in datas[0:-1]:
                name = data['user']['screen_name']
                content = data['text_raw']
                time = data['created_at']
                print(name, time, content)
                csv_writer.writerow([name, time, content])



