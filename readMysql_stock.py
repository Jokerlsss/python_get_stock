from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
import connect_mysql

# --------------------------------- 连接 mysql  ---------------------------------

def getcontent():
    # 参数配置
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stock_data')
    # 建立连接
    con = engine.connect()

    # 创建 session 类型
    DBSession =sessionmaker(bind=engine)
    # 创建 session 对象
    session=DBSession()

    stock_info=session.query()

if __name__ == '__main__':
    getcontent()