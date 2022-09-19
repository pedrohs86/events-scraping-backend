FROM python:3.9.4
ENV FLASK_ENV = production
WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 8000