import redis
import sqlalchemy
from sqlalchemy.orm import sessionmaker


def get_redis_conn(conf, db):
    host = conf.get('redis', 'host')
    pwd = conf.get('redis', 'password')
    port = conf.get('redis', 'port')
    return redis.Redis(connection_pool=redis.ConnectionPool(host=host, port=port, db=db, password=pwd))


def get_db_conn(conf):
    host = conf.get('database', 'host')
    user = conf.get('database', 'user')
    pwd = conf.get('database', 'password')
    db_name = conf.get('database', 'db_name')
    engine = sqlalchemy.create_engine("mysql+pymysql://{user}:{password}@{host}/{db_name}".format(
        user=user, password=pwd, host=host, db_name=db_name), encoding="utf8", echo=True)
    session = sessionmaker(bind=engine, autocommit=True)()

    return session
    # a = WeatherData(city_id=101010300,weather_time=2)
    # session.add(a)
    # session.commit()
    # session.close()

#
# if __name__ == '__main__':
#     conf = ConfigParser.ConfigParser()
#     conf.read('../config.ini')
#     get_db_conn(conf)
