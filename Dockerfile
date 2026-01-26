FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install zabbix-sender binary if needed for advanced features (like PSK with py-zabbix or ensuring compatibility)
# Although py-zabbix is pure python, having the utils is often useful.
RUN apt-get update && apt-get install -y zabbix-sender && rm -rf /var/lib/apt/lists/*

COPY . .

# Environment variables should be passed at runtime
CMD ["python", "main.py"]
