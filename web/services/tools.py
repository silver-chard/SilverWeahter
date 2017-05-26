import ConfigParser

import redis
import sqlalchemy
from sqlalchemy.orm import sessionmaker


def get_redis(conf, db):
    return redis.Redis(
        connection_pool=redis.ConnectionPool(
            host=conf.get('redis', 'host'),
            port=conf.get('redis', 'port'),
            db=db,
            password=conf.get('redis', 'password')
        )
    )


def get_conf(conf_path='sys/config/config.ini'):
    conf = ConfigParser.ConfigParser()
    conf.read(conf_path)
    if not conf.sections():
        return None
    return conf


def get_session(conf=None):
    if not conf:
        conf = get_conf()
        if not conf:
            return None
    host = conf.get('database', 'host')
    user = conf.get('database', 'user')
    pwd = conf.get('database', 'password')
    db_name = conf.get('database', 'db_name')
    engine = sqlalchemy.create_engine("mysql+pymysql://{user}:{password}@{host}/{db_name}".format(
        user=user, password=pwd, host=host, db_name=db_name), encoding="utf8")
    session = sessionmaker(bind=engine)

    return session()
