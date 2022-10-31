FROM python:3.7-alpine
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN mkdir /images
WORKDIR /code/bookmark_api
ADD ./requirements.txt /code/bookmark_api/requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers py3-pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]