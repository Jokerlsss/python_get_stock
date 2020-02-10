from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.types import NVARCHAR, Float, Integer

engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')
con = engine.connect()

BaseModel = declarative_base()

# 获取 database 的所有 table
BaseModel.metadata.reflect(engine)
tables = BaseModel.metadata.tables

# 获取所有 table 名称
tables_names = []
for tb_name in tables.keys():
    # 遍历出每个股票，如 三全食品(002216) ，剔除 users 表
    if tb_name != 'users':
        tables_names.append(tb_name)

df = pd.DataFrame()
# 写入股票全称，包括名字和代码，如：三全食品(002216)
df['股票全称'] = tables_names
# 写入股票名称，如：三全食品
df['股票名称']=list(map(lambda x:x.split('(')[0],tables_names))
# 写入股票代码列，如：002216
# lambda 定义了匿名函数，x 为入口参数，冒号后面为 函数体
# split('(')[1] : 提取出 ‘(’ 之后的内容，若参数为 [0]，则为 ‘(’ 之前的内容
df['股票代码'] = list(map(lambda x: x.split('(')[1].split(')')[0], tables_names))


def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict


# 写入 MySql
df.to_sql(name='StockData', con=con, if_exists='replace', index=False, dtype=map_types(df))
print('Success import.')
con.close()
