FROM python:3.7-slim

WORKDIR /work/app

RUN apt-get update && \
	apt-get install -y build-essential g++ libopencv-dev

COPY keras.json /root/.keras/keras.json

RUN pip install h5py keras==1.2.2 opencv-python theano==0.9 tqdm
