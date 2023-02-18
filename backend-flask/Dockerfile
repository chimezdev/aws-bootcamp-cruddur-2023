FROM python:3.10-slim-buster

# Inside Container / make the folder 'backend-flask '
WORKDIR /backend-flask

# Outside Container -> Inside Container

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# first '.' means everything inside the backend-flask folder outside container into the 'backend-flask' folder inside the container
COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}

# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
