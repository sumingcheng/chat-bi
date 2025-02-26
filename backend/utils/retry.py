import asyncio
from functools import wraps
from typing import Callable, Any, TypeVar
from backend.journal.logging import logger

T = TypeVar('T')

def with_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    重试装饰器
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            retries = 0
            current_delay = delay

            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"重试{max_retries}次后失败: {str(e)}")
                        raise

                    logger.warning(f"第{retries}次重试, 错误: {str(e)}")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator 