# mysql-mcp-server

一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 MySQL 只读查询 MCP 服务，让 AI 助手能够安全地探索和查询 MySQL 数据库。

## 功能

| Tool | 描述 | 参数 |
|------|------|------|
| `list_databases` | 列出当前 MySQL 实例中的所有数据库 | 无 |
| `list_tables` | 列出指定数据库中的所有表 | `db_name?: str` — 数据库名，不传则使用环境变量 `DB_NAME` |
| `get_table_schema` | 获取指定表的结构（列名、数据类型等） | `table_name: str`、`db_name?: str` |
| `execute_read_query` | 执行只读 SELECT 查询并返回结果（最多 100 行） | `query: str`、`db_name?: str` |

> **安全说明**：`execute_read_query` 仅允许以 `SELECT` 开头的语句，拒绝任何写操作。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DB_HOST` | `localhost` | MySQL 主机地址 |
| `DB_PORT` | `3306` | MySQL 端口 |
| `DB_USER` | *(必填)* | 数据库用户名 |
| `DB_PASSWORD` | *(必填)* | 数据库密码 |
| `DB_NAME` | `db` | 默认数据库名 |

## 依赖

| 依赖 | 说明 |
|------|------|
| `fastmcp` | MCP 服务框架 |
| `pymysql` | MySQL 驱动 |

## 快速开始

### 构建 Docker 镜像

```bash
cd mysql_mcp_server
docker build -t mysql-mcp-server .
```

### 集成到 Claude Code

#### 全局（对所有项目生效）

```bash
claude mcp add mysql-mcp-server -s user -- \
  docker run --rm -i \
  -e DB_HOST=<host> \
  -e DB_PORT=3306 \
  -e DB_USER=<user> \
  -e DB_PASSWORD=<password> \
  -e DB_NAME=<database> \
  mysql-mcp-server
```

#### 项目级（仅对当前项目生效）

在项目根目录下执行：

```bash
claude mcp add mysql-mcp-server -s project -- \
  docker run --rm -i \
  -e DB_HOST=<host> \
  -e DB_PORT=3306 \
  -e DB_USER=<user> \
  -e DB_PASSWORD=<password> \
  -e DB_NAME=<database> \
  mysql-mcp-server
```

## 项目结构

```
mysql_mcp_server/
├── mysql_mcp_server.py  # MCP 服务主程序
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 构建文件
└── README.md
```
