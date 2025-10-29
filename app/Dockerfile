#referencias https://fastapi.tiangolo.com/es/deployment/docker/?h=dock#crear-el-codigo-de-fastapi
FROM python:3.12.3-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app
COPY ./models.py /code/
COPY ./db.py /code/

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]