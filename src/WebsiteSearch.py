import os
import re
import urllib.request
from urllib.parse import quote
import random
import datetime



my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
searchEngList = [
    ('https://www.google.com/search?q=', r'search[\s\S]*'),
    ('http://www.baidu.com/s?wd=', ''),
    ('https://cn.bing.com/search?q=', r'aria-label="搜索结果"[\s\S]*')
]
matchRule = r'https?://[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.jp'
# r'https?://[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.jp'


def newfile(filename):
    file = open('data\\%s' % filename, 'w', encoding='utf-8')
    file.close()


def write2file(filename, data):
    file = open('data\\%s' % filename, 'a', encoding='utf-8')
    file.write(data)
    file.close()


def getwebsitebygoogle(name):
    web = 'Not Find'
    i = 0
    while i < 20:
        i += 1
        url = searchAddr + quote(name)

        headers = {'User-Agent': random.choice(my_headers)}
        req = urllib.request.Request(url=url, headers=headers)

        response = urllib.request.urlopen(req)

        html=''
        try:
            html = response.read().decode('utf-8')
        except:
            write2file('errorweb.html', html)

        addr = None
        try:
            addr = re.search(matchRule, re.search(prevText, html).group())
        except:
            pass
        if addr is not None:
            web = addr.group()
            return web
    return web


# Main Program Start

targetList = 'university_JP'
print('目标搜索文件:%s' % targetList)  # 输出提示信息

findlist = open('data\\' + targetList + '.txt', 'r', encoding='utf-8')  # 读取文件

timeCode = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")  # 时间戳

filename = 'outputData_%s_%s.txt' % (targetList, timeCode)  # 组合文件名

newfile(filename)  # 生成文件

index = int(input('请输入选择的搜索引擎(0=Google|1=Baidu|2=Bing):')) % 3  # 选择搜索引擎和表达式
searchAddr = searchEngList[index][0]
prevText = searchEngList[index][1]

print('================开始爬取网址==================\n\n')

os.system('pause')

n = 1


for name in findlist:
    # os.system('cls')
    name = name.partition('\n')[0]
    print('# %d  \t\n搜索大学:%s\n' % (n, name))

    website = 'Error'
    # try:
    #     website = getwebsitebygoogle(name)  # 尝试搜索地址
    # except:
    #     print('Error')

    website = getwebsitebygoogle(name)

    print('搜索结果:%s\n' % website)
    # print('人工确认结果(Y:正确|N:不正确|X强制退出程序):')

    # key = ord(msvcrt.getch())

    # if key == ord('y'):
    #     info = '#%-4d%s : %s\n' % (n, name.ljust(20, chr(12288)), website)
    #     write2file(filename,info)
    #     os.system('cls')
    # elif key == ord('x'):
    #     break
    # else:
    #     info = '#%-4d%s : %s\n' % (n, name.ljust(20, chr(12288)), 'Failed!')
    #     write2file(filename, info)
    #     os.system('cls')

    info = '#%4d%s : %s\n' % (n, name.ljust(20, chr(12288)), website)
    write2file(filename, info)

    n += 1

# os.system('cls')
findlist.close()
print('done!')

os.system("pause")
