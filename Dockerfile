# Local gevent deployment for async development - not the same as on RasPi
FROM python:3.9

# RUN apt-get update
# RUN apt-get install -y libgl1-mesa-glx

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD . /

CMD python3 app.py