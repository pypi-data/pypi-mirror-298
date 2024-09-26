import redis


class FastZDPRedisClient:
    def __init__(
            self,
            host="127.0.0.1",
            port=6379,
            db=0,
            decode_responses=True
    ):
        # 连接池
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=decode_responses)

    def get_client(self):
        """
        从连接池获取客户端对象
        :return: Redis操作的客户端对象
        """
        return redis.Redis(connection_pool=self.pool)

    def set(self, key, value, ex=None):
        """设置字符串的方法"""
        r = self.get_client()
        if isinstance(ex, int):
            r.set(key, value, ex)
        else:
            r.set(key, value)
        r.close()

    def get(self, key):
        """获取字符串的方法"""
        r = self.get_client()
        value = r.get(key)
        r.close()
        return value
