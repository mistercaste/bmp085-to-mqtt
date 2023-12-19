FROM arm32v7/python:3.9 AS builder
RUN mkdir /install
WORKDIR /install
COPY app/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM arm32v7/python:3.9-slim
COPY --from=builder /install /usr/local
COPY /app /app
WORKDIR /app
CMD ["python3", "app.py"]
