# Description:获取西刺IP地址

import requests
from bs4 import BeautifulSoup as bs
import threading
import time

def get_ip(page_num):
    # 请求头进行伪装
    headers = {
        'User-Agent': 'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome / 79.0.3945.130MobileSafari / 537.36'
    }
    # 处理翻页
    url = 'https://www.xicidaili.com/nn'+'/'+str(page_num)
    ip_res = requests.get(url, headers=headers).content.decode('utf-8')
    # 用 lxml 速度较快
    soup = bs(ip_res, 'lxml')
    all = soup.find_all('tr', class_='odd')
    for i in all:
        temp = i.find_all('td')

        # ip + 端口号 = 实际ip地址
        all_ip = temp[1].text + ':' + temp[2].text

        # 验证ip可用性
        # 注意：ip 中有不同类型，如 HTTP 和 HTTPS
        proxies = {
            'http': 'http://' + all_ip,
            'https': 'https://' + all_ip
        }

        # 用于测试的 url
        # proxies ：用于访问的 ip ，若未设置，默认为本机
        # timeout ：等待服务器响应，超时则报错，5是5秒的意思
        texturl = 'http://www.baidu.com'

        # 使用 try 来进行异常处理
        try:
            code_res = requests.get(texturl, proxies=proxies, headers=headers, timeout=5).status_code
            if code_res == 200:
                # 4.保存数据
                print(all_ip)
                # 不放在 for 循环中为了让文件不会重复打开，节约资源
                # with open 可以自动判断何时关闭文件
                # 如果文件一直打开着，且没flush，会导致内容写不进文本文件
                with open('ip_more.txt', 'a', encoding='utf-8') as f:
                    f.write(all_ip + '\n')
        except:
            print('next one =>')

#开始时间
start_time=time.time()

for page in range(1,100):
    # page1+=1
    print('-------------------------正在爬取第{}页-------------------------'.format(page))
    # 多线程
    threading.Thread(target=get_ip,args=(page,)).start()

# 让线程进入死循环
while len(threading.enumerate()) > 1:
    pass
# print('总共的运行时间：',time.time()-start_time,'s',sep=' ')