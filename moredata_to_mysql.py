# Description:将更多的股票 csv 文件导入mysql

import pandas as pd
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, BigInteger
import datetime

# --------------------------------- 连接 mysql  ---------------------------------

# 参数配置
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')
# 建立连接
con = engine.connect()

# --------------------------------- 获取股票数据  ---------------------------------

stock_list = os.listdir('stock_data')

# 随机选择 100 个股票代码
# 同样的 seed 值，随机数一样
random.seed(30)
# 在 list 中随机选择 100 项
files = random.sample(stock_list, 100)


def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: BigInteger()})  # 成交量过大，需用 BigInt
    return dtypedict


# --------------------------------- 保存进 mysql  ---------------------------------

def save_mysql(file):
    path=r'stock_data/{}'.format(file)
    f=open(path,'rb')

    df = pd.read_csv(f, encoding='gbk', usecols=[0, 3, 4, 5, 6, 11], parse_dates=['日期'])
    dtypedict = {}
    # 去掉一些退市或长期停牌的股票
    if all([df['日期'][0] > datetime.datetime.strptime('2010-01-01', "%Y-%m-%d"), df['收盘价'][:50].mean() > 1]):
        if not dtypedict:
            dtypedict = map_types(df)
        # 通过 dtype 设置类型为 dict 格式{"col_name":type}
        df.to_sql(name=file.split('.')[0], con=con, if_exists='replace', index=False, dtype=dtypedict)
        print('------{}已经存入mysql-----'.format(file.split('.')[0]))


# --------------------------------- 运行  ---------------------------------
count=0
for file in files:
    count+=1
    save_mysql(file)
print('总共存入{}个'.format(count))
# 关闭连接
con.close()
