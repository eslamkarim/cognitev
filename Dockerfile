FROM ubuntu:16.04

RUN  apt-get update && apt-get install -y python3 python3-pip git

RUN pip3 install flask
RUN pip3 install requests

RUN cd ~/ &&\
    git clone https://github.com/eslamkarim/cognitev.git server &&\
    cd server 

ENTRYPOINT ["python3"]
CMD ["app.py"]	

