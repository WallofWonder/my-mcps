# 使用官方 Python 3.12 精简镜像作为基础镜像，slim 版本体积更小
FROM python:3.12-slim

# 设置容器内的工作目录，后续命令都在此目录下执行
WORKDIR /app

# 先单独复制依赖文件，利用 Docker 层缓存：只要 requirements.txt 不变，依赖层就不会重新构建
COPY requirements.txt .
# 安装 Python 依赖，--no-cache-dir 避免缓存 pip 下载文件以减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 将 MCP 服务器主程序复制到工作目录
COPY my_mcp_server.py .

# 禁用 Python 输出缓冲，确保 stdio 通信实时传输
ENV PYTHONUNBUFFERED=1

# 容器启动时执行的默认命令，运行 MCP 服务器
CMD ["python", "my_mcp_server.py"]
