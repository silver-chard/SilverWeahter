# coding=utf-8
import sqlalchemy
from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_Session():
    host = '139.199.96.184'
    user = 'root'
    pwd = 'silver'
    db_name = 'test_db'
    engine = sqlalchemy.create_engine("mysql+pymysql://{user}:{password}@{host}/{db_name}".format(
        user=user, password=pwd, host=host, db_name=db_name), encoding="utf8")
    session = sessionmaker(bind=engine)

    return session()


base = declarative_base()


class TestTable(base):
    __tablename__ = 'test_tables'

    # 表的结构:
    name = Column(VARCHAR(255))
    id = Column(INTEGER, primary_key=True, autoincrement=True)


if __name__ == '__main__':
    session = get_db_Session()
    result = session.query(TestTable).filter(TestTable.id == 2).all()
    result[0].name="aaa"
    session.commit()
