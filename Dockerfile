FROM python:3.4.2
WORKDIR /conway
COPY . /conway
RUN pip install -r ./requirements.txt
