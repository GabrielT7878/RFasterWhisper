FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt; apt install ffmpeg

CMD ["python", "/app/main.py"]

EXPOSE 8080