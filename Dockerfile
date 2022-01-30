FROM python:3.7-alpine
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /code
ADD bookmark_api /code/bookmark_api
RUN apk add --no-cache gcc musl-dev linux-headers py3-pip
WORKDIR /code/bookmark_api
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]