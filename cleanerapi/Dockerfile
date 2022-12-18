FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/cln_api

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6

COPY ./req.txt /usr/src/req.txt

RUN pip install -r /usr/src/req.txt

COPY . /usr/src/cln_api

EXPOSE 4000

CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]