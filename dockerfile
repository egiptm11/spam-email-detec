FROM python:3.10

WORKDIR /main

ADD requirements.txt /main/

ADD . /main/ 
RUN pip install -r requirements.txt
ENV UNCERTAINTY_THRESHOLD=0.6

CMD ["python", "main.py"]