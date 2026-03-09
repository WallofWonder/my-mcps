import os
import pymysql
from fastmcp import FastMCP

# 初始化 FastMCP 服务
mcp = FastMCP("mysql-mcp-server")

# 从环境变量获取数据库配置，并设置默认值
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "db")
DB_PORT = int(os.environ.get("DB_PORT", 3306))


def resolve_db_name(db_name: str | None = None) -> str:
    """解析本次调用应使用的数据库名。"""
    return db_name if db_name else DB_NAME


def get_connection(db_name: str | None = None, include_database: bool = True):
    """创建 MySQL 连接。include_database=False 时不指定默认数据库。"""
    connection_kwargs = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "port": DB_PORT,
        "cursorclass": pymysql.cursors.DictCursor,  # 返回字典格式的数据，更适合 AI 理解
    }
    if include_database:
        connection_kwargs["database"] = resolve_db_name(db_name)
    return pymysql.connect(**connection_kwargs)


@mcp.tool
def list_databases() -> str:
    """列出当前 MySQL 实例中的所有数据库。"""
    try:
        connection = get_connection(include_database=False)
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
        connection.close()
        return str(databases)
    except Exception as e:
        return f"Error listing databases: {e}"


@mcp.tool
def list_tables(db_name: str | None = None) -> str:
    """
    列出指定数据库中的所有表。
    参数:
        db_name: 可选数据库名；不传则回退到环境变量 DB_NAME
    """
    target_db = resolve_db_name(db_name)
    try:
        connection = get_connection(db_name=db_name)
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
        connection.close()
        return str(tables)
    except Exception as e:
        return f"Error querying tables from database '{target_db}': {e}"


@mcp.tool
def get_table_schema(table_name: str, db_name: str | None = None) -> str:
    """
    获取指定表的结构（列名、数据类型等）。
    参数:
        table_name: 要查询的表名
        db_name: 可选数据库名；不传则回退到环境变量 DB_NAME
    """
    target_db = resolve_db_name(db_name)
    try:
        connection = get_connection(db_name=db_name)
        with connection.cursor() as cursor:
            # TODO 注意：在生产环境中应严格验证 table_name 以防止 SQL 注入
            cursor.execute(f"DESCRIBE {table_name}")
            schema = cursor.fetchall()
        connection.close()
        return str(schema)
    except Exception as e:
        return f"Error retrieving schema for {table_name} from database '{target_db}': {e}"


@mcp.tool
def execute_read_query(query: str, db_name: str | None = None) -> str:
    """
    执行一个只读的 SQL 查询 (SELECT) 并返回结果。
    参数:
        query: 要执行的 SELECT SQL 语句
        db_name: 可选数据库名；不传则回退到环境变量 DB_NAME
    """
    # 简单的安全校验：只允许 SELECT 语句
    if not query.strip().upper().startswith("SELECT"):
        return "Error: Security restricted. Only SELECT queries are allowed."

    target_db = resolve_db_name(db_name)
    try:
        connection = get_connection(db_name=db_name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            # 限制返回行数以免上下文溢出
            results = cursor.fetchmany(100)
        connection.close()
        return str(results)
    except Exception as e:
        return f"Error executing query on database '{target_db}': {e}"


if __name__ == "__main__":
    # 默认使用 stdio 传输层运行服务（这是集成到客户端的最常用方式）
    mcp.run()
