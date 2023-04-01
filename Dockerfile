FROM python:3.9.16-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod +x ./run.sh
ENV PORT 8000
ENTRYPOINT ["./run.sh"]
