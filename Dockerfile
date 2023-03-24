FROM python:3.8



# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src


#to COPY the remote file at working directory in container
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . . 

VOLUME [ "/data" ]


CMD [ "python", "./main.py"]