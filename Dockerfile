# 使用官方 Python 基礎映像
FROM python:3.11-slim

# 設定容器中的工作目錄
WORKDIR /app

# 複製目前所有檔案到容器中
COPY . /app

# 安裝套件（根據 requirements.txt）
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Flask 使用的 port
EXPOSE 5550

# 啟動應用程式
CMD ["python", "shortenUrl.py"]
