FROM python:3.9.1

WORKDIR /usr/src/app

RUN apt update && \
    apt install -y cmake

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]
