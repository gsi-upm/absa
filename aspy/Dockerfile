FROM gsiupm/senpy:0.6.2-python3.4

RUN apt-get update
RUN apt-get -y install libopenblas-dev
RUN apt-get -y install gfortran
RUN apt-get -y install libxml2-dev libxslt1-dev python-dev


ADD requirements.txt /senpy-plugins/
RUN pip install -r /senpy-plugins/requirements.txt

ADD / /senpy-plugins/aspy

WORKDIR /usr/src/app/

ENTRYPOINT ["python", "-m", "senpy", "-f", "/senpy-plugins", "--host", "0.0.0.0"]