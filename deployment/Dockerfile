FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8000