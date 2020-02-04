# Description: 获取股票编码

import requests
import random
from bs4 import BeautifulSoup as bs
import time
import redis


rds = redis.from_url('redis://:123456@175.24.66.216:6379',db=1,decode_responses=True)

def get_stock_names():
    # rds=redis.Redis(host="175.24.66.216", port=6379, password="123456")
    url = "http://quote.eastmoney.com/stock_list.html#"
    headers = {
        'Referer':'http://quote.eastmoney.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    response = requests.get(url,headers=headers).content.decode('gbk')
    soup = bs(response,'lxml')
    all_ul=soup.find('div',id='quotesearch').find_all('ul')
    # print('all_ul',all_ul)

    # with open('stock_names.txt','w+',encoding='utf-8') as f:
    #     for ul in all_ul:
    #         all_a=ul.find_all('a')
    #         for a in all_a:
    #             rds.rpush('stock_names',a.text)
    #             f.write(a.text+'\n')
    #             print(a.text)
    print('Finish to Get')

def get_data():
    headers={
        'Referer':'http://quotes.money.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    while True:
        # redis 上获取 股票名
        stock_name = rds.lpop('stock_names')
        if stock_name:
            try:
                stock_code=stock_name.split('(')[1].split(')')[0]
                # 由于东方财富网上获取的代码一部分为基金，无法获取数据，故将基金剔除掉。
                # 沪市股票以6,9开头，深市以0,2,3开头，但是部分基金也是2开头，201/202/203/204这些也是基金
                # 另外获取data的网址股票代码 沪市前加0， 深市前加1
                if int(stock_code[0]) in [0,2,3,6,9]:
                    if int(stock_code[0]) in [6,9]:
                        stock_code_new='0'+stock_code
                    elif int(stock_code[0]) in [0,2,3]:
                        if not int(stock_code[:3]) in [201,202,203,204]:
                            stock_code_new='1'+stock_code
                        else:continue
                    else:continue
                else:continue

                stock_url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(stock_code)
                response=requests.get(stock_url,headers=headers).text
                soup=bs(response,'lxml')

                # 获取起始时间
                # start_time=soup.find('input',{'name':'date_start_type'}).get('value').replace('-','')
                #获取结束时间
                # end_time=soup.find('input',{'name':'date_start_type'}).get('value').replace('-','')


                # 让爬虫随机停顿 1-2 s
                time.sleep(random.choice([1,2]))
                download_url="http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(stock_code_new, start_time_input, end_time_input)
                data=requests.get(download_url,headers=headers)
                with open('stock_data/{}.csv'.format(stock_name),'wb') as f:
                    for chunk in data.iter_content(chunk_size=10000):
                        if chunk:
                            f.write(chunk)
                print('{}数据已经下载完成'.format(stock_name))
            except Exception as e:
                rds.rpush('stock_names',stock_name)
                print(e)
        else:break

# 通过控制台输入 开始时间 和 结束时间
print('Enter a StartTime,like as 20010101:')
start_time_input=input()
print('Enter a EndTime,like as 20010101:')
end_time_input=input()

# 调用函数
get_stock_names()
get_data()