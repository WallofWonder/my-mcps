# MCP Servers

基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 MCP（Model Context Protocol）服务集合，可通过 Docker 一键部署并集成到 Claude Code 等 AI 客户端。

## 服务目录

| 服务 | 描述 | 文档 |
|------|------|------|
| [my-mcp-server](./my_mcp_server/) | 入门示例：一个最简单的问候 Tool | [README](./my_mcp_server/README.md) |
| [mysql-mcp-server](./mysql_mcp_server/) | MySQL 只读查询：让 AI 探索和查询数据库 | [README](./mysql_mcp_server/README.md) |

## 快速上手

每个 MCP 服务均提供 Docker 镜像，无需在本地安装任何 Python 依赖。

1. 进入对应目录，按照 README 构建镜像
2. 使用 `claude mcp add` 将服务注册到 Claude Code
3. 在对话中直接调用对应 Tool

## 技术栈

- **运行时**：Python 3.12
- **MCP 框架**：[FastMCP](https://github.com/jlowin/fastmcp)
- **部署方式**：Docker（stdio 传输层）

## 说明

本仓库文档的部分内容通过 [Claude Code](https://claude.ai/claude-code) 生成。
