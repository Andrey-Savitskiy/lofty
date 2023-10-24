FROM python:3

WORKDIR /save_to_db
COPY ./requirements.txt /save_to_db/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY ./save_to_db /save_to_db

CMD ["python3", "save_to_db.py"]