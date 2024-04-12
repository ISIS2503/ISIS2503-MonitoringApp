FROM python:3

WORKDIR /usr/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "makemigrations" ]
CMD [ "python", "manage.py", "migrate" ]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]