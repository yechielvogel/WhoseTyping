FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

# RUN apt-get update && apt-get install -y \
#     xvfb \
#     x11-utils

EXPOSE 80

CMD ["python3", "main.py"]