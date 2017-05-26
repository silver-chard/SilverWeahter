from services.tools import get_redis, get_conf


def get_province():
    conf = get_conf( )
    if conf:
        redis = get_redis(conf, conf.getint('redis', 'city_list_redis'))
        provinces = redis.keys('china_*')
        return {redis.get(p): p.split('_')[1] for p in provinces}
    return None

def get_city_id(province_id):
    redis = get_redis(get_conf(), get_conf().getint('redis', 'city_list_redis'))
    cities = redis.keys('city_{province}_*'.format(province=province_id))
    if len(cities)> 0:
        return {redis.get(c): c.split('_')[2] for c in cities}
    else:
        cities = redis.keys('station_{province}_*'.format(province=province_id))
        return {redis.get(c): c.split('_')[2] for c in cities}


def get_station_id(province_id, city_id):
    redis = get_redis(get_conf(), get_conf().getint('redis', 'city_list_redis'))
    print 'station_{province}_{city}_*'.format(province=province_id, city=city_id)
    stations = redis.keys('station_{province}_{city}_*'.format(province=province_id, city=city_id))
    return {redis.get(s): s.split('_')[3] for s in stations}

#
# if __name__ == '__main__':
#     print get_province()
#     print get_city_id(10126)
#     s = get_station_id(10126, '02')
#     print s
#     # for city in citys:
#     #     print city
#     pass
