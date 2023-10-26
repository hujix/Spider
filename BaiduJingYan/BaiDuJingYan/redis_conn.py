import redis

host = "host"
password = "pwd"
port = 9379
database = 10

redis_conn = redis.Redis(host=host, port=port, password=password, db=database, decode_responses=True)


def redis_check_exist(file_id) -> bool:
    redis_data = redis_conn.get(file_id)
    if redis_data is None:
        return False
    return True


def redis_save_cache(file_id, data) -> bool:
    return redis_conn.set(file_id, data, ex=60 * 60 * 24 * 365)
