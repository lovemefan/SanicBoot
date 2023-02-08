FROM python:3.8.5-slim

COPY . /SanicExample/backend

COPY requirements.txt /SanicExample/backend

WORKDIR /SanicExample/backend
EXPOSE 80
RUN python3 -m pip install --upgrade pip && pip3 install -r "/SanicExample/backend/requirements.txt" -i "https://pypi.tuna.tsinghua.edu.cn/simple"

CMD ["python3", "/SanicExample/backend/app.py"]
