FROM python:3.9.5
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./data
CMD ["python", "./prices.py"]