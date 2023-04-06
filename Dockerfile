FROM python:3.9

WORKDIR /code/

RUN pip install pipenv

# COPY ../Pipfile /code/
COPY ./.env /code/.env
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN pipenv requirements > requirements.txt

# COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./backend/ /code/backend/

# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]