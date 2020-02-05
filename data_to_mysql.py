# Description：将一个 csv 文件导入 mysql
# 参考链接：https://blog.csdn.net/tonydz0523/article/details/82529941

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.types import NVARCHAR, FLOAT, INTEGER

# ----------------------------- ① sqlalchemy 连接 mysql 方法 ----------------------------------

# 参数配置
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')
# 建立连接
con = engine.connect()

# ---------------------------------- ② Mysql 连接方法 ----------------------------------

# 参数设置 DictCursor 使输出为字典模式，链接到本地数据库 root 123456
# config=dict(host='localhost',user='root',password='123456',
#             cursorclass=pymysql.cursors.DictCursor)
# # 建立连接
# conn=pymysql.Connect(**config)
# # 自动确认 commit True
# conn.autocommit(1)
# # 设置光标
# cursor=conn.cursor()

# --------------------------------- 读取 csv 文件 ---------------------------------

# usecols 只用这些列，其他列不需要
# parse_dates 由于csv只储存str、int、float格式无法储存日期格式，所以读取是把日期列读作时间格式
# def save_mysql():
df = pd.read_csv('sevenstock.csv', encoding='gbk', usecols=[0, 3, 4, 5, 6, 11], parse_dates=['日期'])


# -------------------------------- ② mysql 方式的格式转换 --------------------------------

# 一个根据pandas自动识别type来设定table的type
# def make_table_sql(df):
#     colums=df.colums.tolist()
#     types=df.ftypes
#     # 添加 id 自动递增
#     make_table=[]
#     for item in colums:
#         if 'int' in types[item]:
#             char=item+'INT'
#         elif 'float' in types[item]:
#             char=item+'FLOAT'
#         elif 'object' in types[item]:
#             char=item+'VARCHAR(255)'
#         elif 'datetime' in types[item]:
#             char=item+'DATETIME'
#         make_table.append(char)
#     return ','.join(make_table)

# -------------------------------- ① sqlalchemy 方式的格式转换 --------------------------------

# pandas 和 sql 类型转换
def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: FLOAT(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: INTEGER()})
    return dtypedict


# ------------------------------ ① 存入 mysql  ------------------------------

dtypedict = map_types(df)
# 通过 dtype 设置类型为 dict 格式 {"col_name":type}
df.to_sql(name='seven', con=con, if_exists='replace', index=False, dtype=dtypedict)

# ------------------------- ② 创建 table 并批量写入 mysql -------------------------
