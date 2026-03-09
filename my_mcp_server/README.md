# my-mcp-server

一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的入门级 MCP 服务示例，演示如何创建并注册一个最简单的 MCP Tool。

## 功能

| Tool | 描述 | 参数 |
|------|------|------|
| `greet` | 返回一条问候语 | `name: str` — 被问候的名字 |

## 依赖

| 依赖 | 说明 |
|------|------|
| `fastmcp` | MCP 服务框架 |

## 快速开始

### 构建 Docker 镜像

```bash
cd my_mcp_server
docker build -t my-mcp-server .
```

### 集成到 Claude Code

#### 全局（对所有项目生效）

```bash
claude mcp add my-mcp-server -s user -- \
  docker run --rm -i my-mcp-server
```

#### 项目级（仅对当前项目生效）

在项目根目录下执行：

```bash
claude mcp add my-mcp-server -s project -- \
  docker run --rm -i my-mcp-server
```

## 项目结构

```
my_mcp_server/
├── my_mcp_server.py   # MCP 服务主程序
├── requirements.txt   # Python 依赖
├── Dockerfile         # Docker 构建文件
└── README.md
```
