#!/usr/bin/env python3

import asyncio
import aioredis

class DpowRedis(object):

    def __init__(self, server, loop):
        self.pool = aioredis.create_pool(
            server,
            minsize=5, maxsize=15,
            loop=loop
        )

    async def setup(self):
        self.pool = await self.pool

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def insert(self, key: str, value: str):
        return await self.pool.execute('set', key, value )

    async def delete(self, key: str):
        return await self.pool.execute('del', key)

    async def get(self, key: str):
        val = await self.pool.execute('get', key)
        return val.decode("utf-8") if val else None

    async def exists(self, key: str):
        exists = await self.pool.execute('exists', key)
        return exists == 1

    async def insert_if_noexist(self, key: str, value: str):
        existed = await self.pool.execute('setnx', key, value)
        return existed == 1

    async def increment(self, key: str):
        return await self.pool.execute('incr', key)

    async def hash_increment(self, key: str, field: str, by=1):
        return await self.pool.execute('hincrby', key, field, by)

    async def hash_getall(self, key: str):
        arr = await self.pool.execute('hgetall', key)
        return {arr[i].decode("utf-8"): arr[i+1].decode("utf-8") for i in range(0, len(arr)-1, 2)}

    async def hash_get(self, key:str, field: str):
        return await self.pool.execute('hget', key, field)

    async def set_add(self, key: str, value: str):
        return await self.pool.execute('sadd', key, value)