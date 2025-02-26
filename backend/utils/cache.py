from aiocache import Cache
from aiocache.serializers import JsonSerializer
from typing import Any, Optional
import json

class QueryCache:
    def __init__(self):
        self.cache = Cache(
            Cache.MEMORY,
            serializer=JsonSerializer(),
            ttl=300,  # 5分钟缓存
            namespace="query"
        )

    async def get(self, query: str, params: Optional[dict] = None) -> Optional[Any]:
        """获取缓存的查询结果"""
        key = self._generate_key(query, params)
        return await self.cache.get(key)

    async def set(self, query: str, result: Any, params: Optional[dict] = None):
        """缓存查询结果"""
        key = self._generate_key(query, params)
        await self.cache.set(key, result)

    async def clear(self):
        """清空缓存"""
        await self.cache.clear()

    def _generate_key(self, query: str, params: Optional[dict] = None) -> str:
        """生成缓存键"""
        key_data = {"query": query}
        if params:
            key_data["params"] = params
        return json.dumps(key_data, sort_keys=True) 