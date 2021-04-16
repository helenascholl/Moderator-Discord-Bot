FROM schollsebastian/python-dlib:3.8-buster

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]
