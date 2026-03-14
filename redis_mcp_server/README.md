# redis-mcp-server

一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 Redis 只读查询 MCP 服务，让 AI 助手能够安全地探索和查询 Redis 数据库。

## 功能

| Tool                 | 描述                                     | 参数                                                         |
|----------------------|----------------------------------------|------------------------------------------------------------|
| `ping`               | 检查 Redis 服务是否可达                        | 无                                                          |
| `get_server_info`    | 获取服务器版本、内存、连接数等信息                      | 无                                                          |
| `list_keys`          | 列出匹配指定模式的 key（基于 SCAN，不阻塞）             | `pattern?: str`（默认 `*`）、`count?: int`（默认 100）              |
| `get_key_type`       | 获取 key 的数据类型                           | `key: str`                                                 |
| `get_key_ttl`        | 获取 key 的剩余过期时间（秒）                      | `key: str`                                                 |
| `get_string`         | 获取 string 类型 key 的值                    | `key: str`                                                 |
| `get_hash`           | 获取 hash 类型 key 的全部字段或指定字段              | `key: str`、`field?: str`                                   |
| `get_list`           | 获取 list 类型 key 的元素（分页）                 | `key: str`、`start?: int`、`stop?: int`                      |
| `get_set_members`    | 获取 set 类型 key 的成员（随机采样）                | `key: str`、`count?: int`（默认 100）                           |
| `get_sorted_set`     | 获取 sorted set (zset) 类型 key 的成员（按分数升序） | `key: str`、`start?: int`、`stop?: int`、`with_scores?: bool` |
| `get_keyspace_stats` | 获取各数据库的 key 数量、过期 key 数等统计信息           | 无                                                          |

> **安全说明**：本服务仅提供只读操作，不暴露任何写入、删除或修改命令，确保 Redis 数据安全。
> 
> Redis 官方提供了全功能的 MCP，详见 https://redis.io/docs/latest/integrate/redis-mcp/

## 环境变量

| 变量                | 默认值            | 说明                |
|-------------------|----------------|-------------------|
| `REDIS_HOST`      | `localhost`    | Redis 主机地址        |
| `REDIS_PORT`      | `6379`         | Redis 端口          |
| `REDIS_PASSWORD`  | *(空)*          | Redis 密码，无密码时可不设置 |
| `REDIS_DB`        | `0`            | 默认数据库编号（0~15）     |

## 依赖

| 依赖        | 说明               |
|-----------|------------------|
| `fastmcp` | MCP 服务框架         |
| `redis`   | Redis Python 客户端 |

## 快速开始

### 构建 Docker 镜像

```bash
cd redis_mcp_server
docker build -t redis-mcp-server .
```

### 集成到 Claude Code

#### 全局（对所有项目生效）

```bash
claude mcp add redis-mcp-server -s user -- \
  docker run --rm -i \
  -e REDIS_HOST=<host> \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD=<password> \
  -e REDIS_DB=0 \
  redis-mcp-server
```

#### 项目级（仅对当前项目生效）

在项目根目录下执行：

```bash
claude mcp add redis-mcp-server -s project -- \
  docker run --rm -i \
  -e REDIS_HOST=<host> \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD=<password> \
  -e REDIS_DB=0 \
  redis-mcp-server
```

#### 访问 docker 网络下的 redis 容器

需要在命令中额外加上 `--network <network>`

`REDIS_HOST` 配置为 redis 容器的名称

示例（访问在 `network1` 网络中名为 `my_redis` 的 redis 容器）：
```bash
claude mcp add redis-mcp-server -s project -- \
  docker run --rm -i \
  -e REDIS_HOST=my_redis \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD=<password> \
  -e REDIS_DB=0 \
  --network network1 \
  redis-mcp-server
```

## 项目结构

```
redis_mcp_server/
├── redis_mcp_server.py  # MCP 服务主程序
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 构建文件
└── README.md
```
