from redis import Redis


def get_redis_conn(host='localhost', port=6379, db='0'):
    """
    获取redis_conn
    """
    redis_conn = Redis(host=host,
                       port=port,
                       db=db)
    return redis_conn
