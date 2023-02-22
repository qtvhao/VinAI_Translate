FROM pytorch/pytorch

WORKDIR /app

RUN apt-get update && apt-get install -y git libsndfile1 sox unzip wget

COPY requirements.txt .

RUN pip3 install -r requirements.txt