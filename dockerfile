FROM python:3

ADD docker.py
RUN pip install boto3
RUN pip install json
CMD [ "python", "./docker.py" ]
