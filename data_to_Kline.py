# Description：将 mysql 中的数据画成 K 线图
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import random
import json
import plotly.offline as po
import plotly.graph_objs as go
import time

from flask_cors import *
from flask import Flask,request
app=Flask(__name__)

@app.route('/get',methods=['GET'])
def get_graph():
    # 连接 mysql
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')
    con = engine.connect()

    BaseModel=declarative_base()

    # 获取 database 的所有 table
    BaseModel.metadata.reflect(engine)
    tables=BaseModel.metadata.tables
    # 获取所有 table 名称
    tables_names=list(tables.keys())

    # 随机选取一只股票
    stock_name=random.choice(tables_names)
    # 获取股票数据
    print(stock_name)
    df=pd.read_sql('select * from `{}` order by 日期 asc'.format(stock_name),con=con)

    # to_json 将数据类型以 values 形式转换为 json 格式
    jsonDF=df.to_json(orient="values",force_ascii=False,date_format="日期")
    # json.loads 将字符串转化为 list
    # json.dumps 将 list 转化为字符串
    jsonToList=json.loads(jsonDF)

    # para用于最终的数据格式呈现，如：[["xxx","yy"],["xx","yy"]]
    para = []
    para.append(stock_name)
    for i in jsonToList:
        # 时间戳多出3个0，为 int 类型，故处理成 除以1000
        timeArray=time.localtime(i[0]/1000)
        # otherTime 为日期格式呈现的数据
        otherTime=time.strftime("%Y-%m-%d",timeArray)
        # 将日期格式的数据替换掉数组中的时间戳
        i[0]=otherTime

        # 将类型为 int 的列表，转化为 str，如 [2019-01-01,24] -> ['2019-01-01','24']
        b=[str(j) for j in i]
        para.append(b)
    # list 不能作为返回值，得先转成 json格式
    print("para:", para[1])
    return json.dumps(para,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5590)


    # ------------------------ 将 K 线图画在 html 文件中----------------------
    # trace=go.Candlestick(x=df['日期'],
    #                      open=df['开盘价'],
    #                      high=df['最高价'],
    #                      low=df['最低价'],
    #                      close=df['收盘价'])
    #
    # data=[trace]
    # layout={
    #     'title':stock_name
    # }
    # fig=dict(data=data,layout=layout)
    # po.plot(fig,filename='stock.html')

