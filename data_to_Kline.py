# Description：将 mysql 中的数据画成 K 线图
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import random
import plotly.offline as po
import plotly.graph_objs as go

def get_graph():
    # 连接 mysql
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')

    BaseModel=declarative_base()

    # 获取 database 的所有 table
    BaseModel.metadata.reflect(engine)
    tables=BaseModel.metadata.tables
    # 获取所有 table 名称
    tables_names=list(tables.keys())
    con=engine.connect()
    # 随机选取一只股票
    stock_name=random.choice(tables_names)
    # 获取股票数据
    df=pd.read_sql('select * from `{}`'.format(stock_name),con=con)

    trace=go.Candlestick(x=df['日期'],
                         open=df['开盘价'],
                         high=df['最高价'],
                         low=df['最低价'],
                         close=df['收盘价'])

    data=[trace]
    layout={
        'title':stock_name
    }
    fig=dict(data=data,layout=layout)
    po.plot(fig,filename='stock.html')


get_graph()
