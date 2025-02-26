from fastapi import Request
import time
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}

    async def check(self, request: Request) -> Tuple[bool, float]:
        client_ip = request.client.host
        now = time.time()
        
        # 清理过期请求记录
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if now - req_time < 60
            ]
        else:
            self.requests[client_ip] = []

        # 检查是否超过限制
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            wait_time = 60 - (now - self.requests[client_ip][0])
            return False, wait_time

        self.requests[client_ip].append(now)
        return True, 0 