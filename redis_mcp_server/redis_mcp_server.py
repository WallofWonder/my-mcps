import os
import redis
from fastmcp import FastMCP

# 初始化 FastMCP 服务
mcp = FastMCP("redis-mcp-server")

# 从环境变量获取 Redis 配置，并设置默认值
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
REDIS_DB = int(os.environ.get("REDIS_DB", 0))


def get_client() -> redis.Redis:
    """创建 Redis 客户端连接。"""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_DB,
        decode_responses=True,  # 返回字符串而非字节，更易读
    )


@mcp.tool
def ping() -> str:
    """检查 Redis 服务是否可达，返回 PONG 表示连接正常。"""
    try:
        client = get_client()
        result = client.ping()
        return "PONG" if result else "No response"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def get_server_info() -> str:
    """获取 Redis 服务器的详细信息（版本、内存、连接数等）。"""
    try:
        client = get_client()
        info = client.info()
        # 筛选最有用的字段
        keys = [
            "redis_version", "redis_mode", "os", "arch_bits",
            "uptime_in_seconds", "connected_clients", "used_memory_human",
            "used_memory_peak_human", "total_commands_processed",
            "keyspace_hits", "keyspace_misses", "role",
        ]
        summary = {k: info[k] for k in keys if k in info}
        return str(summary)
    except Exception as e:
        return f"Error getting server info: {e}"


@mcp.tool
def list_keys(pattern: str = "*", count: int = 100) -> str:
    """
    列出匹配指定模式的 key。
    参数:
        pattern: glob 风格的匹配模式，默认 "*" 表示所有 key
        count:   最多返回的 key 数量，默认 100，最大 1000
    """
    count = min(count, 1000)
    try:
        client = get_client()
        keys = []
        # 使用 SCAN 替代 KEYS，避免阻塞服务器
        for key in client.scan_iter(match=pattern, count=100):
            keys.append(key)
            if len(keys) >= count:
                break
        return str(keys)
    except Exception as e:
        return f"Error listing keys: {e}"


@mcp.tool
def get_key_type(key: str) -> str:
    """
    获取指定 key 的数据类型（string / list / set / zset / hash / stream）。
    参数:
        key: Redis key 名称
    """
    try:
        client = get_client()
        key_type = client.type(key)
        if key_type == "none":
            return f"Key '{key}' does not exist."
        return key_type
    except Exception as e:
        return f"Error getting type for key '{key}': {e}"


@mcp.tool
def get_key_ttl(key: str) -> str:
    """
    获取指定 key 的剩余过期时间（秒）。
    返回 -1 表示永不过期，-2 表示 key 不存在。
    参数:
        key: Redis key 名称
    """
    try:
        client = get_client()
        ttl = client.ttl(key)
        if ttl == -2:
            return f"Key '{key}' does not exist."
        if ttl == -1:
            return f"Key '{key}' has no expiration (persistent)."
        return f"Key '{key}' expires in {ttl} seconds."
    except Exception as e:
        return f"Error getting TTL for key '{key}': {e}"


@mcp.tool
def get_string(key: str) -> str:
    """
    获取 string 类型 key 的值。
    参数:
        key: Redis key 名称
    """
    try:
        client = get_client()
        value = client.get(key)
        if value is None:
            return f"Key '{key}' does not exist or is not a string."
        return value
    except Exception as e:
        return f"Error getting key '{key}': {e}"


@mcp.tool
def get_hash(key: str, field: str | None = None) -> str:
    """
    获取 hash 类型 key 的字段值。
    参数:
        key:   Redis key 名称
        field: 可选，指定字段名；不传则返回所有字段
    """
    try:
        client = get_client()
        if field:
            value = client.hget(key, field)
            if value is None:
                return f"Field '{field}' not found in hash '{key}'."
            return str({field: value})
        else:
            result = client.hgetall(key)
            if not result:
                return f"Hash '{key}' does not exist or is empty."
            return str(result)
    except Exception as e:
        return f"Error getting hash '{key}': {e}"


@mcp.tool
def get_list(key: str, start: int = 0, stop: int = 99) -> str:
    """
    获取 list 类型 key 的元素（分页）。
    参数:
        key:   Redis key 名称
        start: 起始索引，默认 0
        stop:  结束索引（含），默认 99（即最多返回 100 个元素）
    """
    try:
        client = get_client()
        result = client.lrange(key, start, stop)
        if not result:
            return f"List '{key}' does not exist or is empty."
        length = client.llen(key)
        return f"Total length: {length}, elements [{start}:{stop}]: {result}"
    except Exception as e:
        return f"Error getting list '{key}': {e}"


@mcp.tool
def get_set_members(key: str, count: int = 100) -> str:
    """
    获取 set 类型 key 的成员（随机采样，不保证顺序）。
    参数:
        key:   Redis key 名称
        count: 最多返回的成员数，默认 100
    """
    count = min(count, 1000)
    try:
        client = get_client()
        total = client.scard(key)
        if total == 0:
            return f"Set '{key}' does not exist or is empty."
        members = client.srandmember(key, count)
        return f"Total members: {total}, sample (up to {count}): {members}"
    except Exception as e:
        return f"Error getting set '{key}': {e}"


@mcp.tool
def get_sorted_set(key: str, start: int = 0, stop: int = 99, with_scores: bool = True) -> str:
    """
    获取 sorted set (zset) 类型 key 的成员（按分数升序）。
    参数:
        key:         Redis key 名称
        start:       起始排名，默认 0
        stop:        结束排名（含），默认 99
        with_scores: 是否返回分数，默认 True
    """
    try:
        client = get_client()
        total = client.zcard(key)
        if total == 0:
            return f"Sorted set '{key}' does not exist or is empty."
        result = client.zrange(key, start, stop, withscores=with_scores)
        return f"Total members: {total}, range [{start}:{stop}]: {result}"
    except Exception as e:
        return f"Error getting sorted set '{key}': {e}"


@mcp.tool
def get_keyspace_stats() -> str:
    """获取各数据库（db0~dbN）的 key 数量、过期 key 数量等统计信息。"""
    try:
        client = get_client()
        info = client.info("keyspace")
        if not info:
            return "No keyspace data found (Redis may be empty)."
        return str(info)
    except Exception as e:
        return f"Error getting keyspace stats: {e}"


if __name__ == "__main__":
    # 默认使用 stdio 传输层运行服务（这是集成到客户端的最常用方式）
    mcp.run()
