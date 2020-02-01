# Description: 获取股票编码

import requests
import random
from bs4 import BeautifulSoup as bs
import time
import redis

def get_stock_names():
    # rds=redis.Redis(host="175.24.66.216", port=6379, password="123456")
    rds = redis.from_url('redis://:123456@175.24.66.216:6379',db=1,decode_responses=True)
    url = "http://quote.eastmoney.com/stock_list.html#"
    headers = {
        'Referer':'http://quote.eastmoney.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    response = requests.get(url,headers=headers).content.decode('gbk')
    soup = bs(response,'lxml')
    all_ul=soup.find('div',id='quotesearch').find_all('ul')
    print('all_ul',all_ul)
    with open('stock_names.txt','w+',encoding='utf-8') as f:
        for ul in all_ul:
            all_a=ul.find_all('a')
            for a in all_a:
                rds.rpush('stock_names',a.text)
                f.write(a.text+'\n')
    print('Finish to Get')

get_stock_names()