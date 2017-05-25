from services.tools import get_redis, get_conf


def get_province():
    redis = get_redis(get_conf(), get_conf().getint('redis', 'city_list_redis'))
    provinces = redis.keys('china_*')
    return {redis.get(p): p.split('_')[1] for p in provinces}


if __name__ == '__main__':
    print get_province()
