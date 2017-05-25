import ConfigParser

import redis


def get_redis(conf, db):
    return redis.Redis(
        connection_pool=redis.ConnectionPool(
            host=conf.get('redis', 'host'),
            port=conf.get('redis', 'port'),
            db=db,
            password=conf.get('redis', 'password')
        )
    )


def get_conf(conf_path='../sys/config/config.ini'):
    conf = ConfigParser.ConfigParser()
    conf.read(conf_path)
    if not conf.sections():
        return None
    return conf
