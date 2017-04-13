# coding:utf-8
#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import random
import os
import os.path
import sys
"""
作者：LeonTian
行业：会计
年龄：24
学习编程时间：2016年11月26日至今
介绍项目：
1.构造多种请求头文件
2.实现对不同板块的访问
3.完成中文文件的保存
4.用post方式下载
5.指定页码范围下载
6.打包成exe

学习感受：爬1024简直艰难，跳链、中文、post，太考验耐性，
还好结果是好的，总算幸不辱命，能够造福大家。
"""

reload(sys)
sys.setdefaultencoding('utf-8')
# 构造user-agent列表，欺骗目标网站
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def get_request_headers():
    request_headers = {
        'User-Agent': random.choice(UserAgent_List),  #随机选择一个user-agent
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        }
    return request_headers

def get_torrent_headers():
    torrent_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www2.j32048downhostup9s.info',
        'Origin': 'http://www2.j32048downhostup9s.info',
        'Referer': 'http://www2.j32048downhostup9s.info',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(UserAgent_List),
    }
    return torrent_headers

def get_1024_links(id,page):  #  id代表板块，page代表下载的页码
    url = 'http://1024.luj8le.click/pw/thread.php?fid={}&page={}'.format(id,page)  # 构造题目列表的网址
    url1 = 'http://1024.luj8le.click/pw/'
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'  # 避免乱码的情况
    soup = BeautifulSoup(wb_data.text, 'lxml')  # 用lxml进行解析
    links = soup.select('tr.tr3 > td > h3 > a')
    links_1024 = []
    for link in links:
        if 'htm_data' in link.get('href'):
            url = url1 + link.get('href')  # 拼接成帖子的链接
            links_1024.append(url)
    print links_1024
    return links_1024  # 返回这一页50个帖子的链接列表

def get_format_filename(input_filename): # 文件夹的名字不能含有的特殊符号，windows下的限定
    for s in ['?', '*', '<', '>', '\★', '！', ':', '/']:
        while s in input_filename:
            input_filename = input_filename.strip().replace(s, '')
    return input_filename

def gbk(name):  #避免斜杠让系统误解
    name = name.replace('/', unichr(ord('/') + 65248)).replace('\\', unichr(ord('\\') + 65248)).encode('gbk','ignore')
    # ignore是为了避免有gbk没法解码的乱码
    return name

def get_1024_details(url): # 这里接收get_1024_links返回的link链接列表
    wb_date = requests.get(url,headers=get_request_headers()) #
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'lxml')
    wb_date.close()
    print '子页面读取完毕: ' + url
    try:
        filename = soup.select('#subject_tpc')[0].get_text().encode('utf-8','ignore')
        filename = get_format_filename(filename).decode('utf-8','ignore')
        # 网站可能为了反爬，文件名里有\xa0 和 \r,又是一个保存文件的坑
        filename = filename.replace(u'\xa0', u'').replace(u'\r', u'')
        print "正在下载：" + filename
        if not os.path.exists(filename):# windows保存文件的坑，存在了再创建会报错
            os.makedirs(filename)
        try:
            torrent_link = soup.select('#read_tpc > a')[0].get('href')
            get_torrent(torrent_link, filename)
        except IOError:
            print url, filename  # 出错，返回出错链接跟文件名
    except IndexError:
        pass

def get_torrent(torrent_link,filename):
    torrent_download_url = 'http://www2.j32048downhostup9s.info/freeone/down.php'
    s = requests.Session()  # 构造一个会话
    wb_date = s.get(torrent_link, headers=get_request_headers(),timeout=10)
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'lxml')
    wb_date.close()
    data = {}
    for i in soup.select('form input'):
        if i.get('name'):
            data[i.get('name')] = i.get('value')
    torrent = s.post(torrent_download_url, headers=get_torrent_headers(), data=data,timeout=10)
    with open(os.getcwd() + '//'+ filename+'//' + filename + '.torrent', 'wb+') as f:
        f.write(torrent.content)
    torrent.close()

"""
亚洲无码：5
日本骑兵：22
欧美新片：7
三级写真：18
"""
while True:
    id_input = input('请输入下载板块：\n 1.亚洲无码\n 2.日本骑兵\n 3.欧美新片\n 4.三级写真\n 5.退出 ')
    if id_input == 1:
        id_output = 5
    elif id_input == 2:
        id_output = 22
    elif id_input == 3:
        id_output = 7
    elif id_input == 4:
        id_output = 18
    elif id_input == 5:
        break
    page_start = input('请输入起始页码：')
    page_end = input('请输入结束页码：')
    for page_input in xrange(page_start,page_end+1):
        print "开始爬取第{}页".format(page_input)
        list_1024 = get_1024_links(id_output, page_input)
        for i in list_1024:
            get_1024_details(i)
    print "完工啦老司机！\n"
