FROM python:3

WORKDIR /parser
COPY ./requirements.txt /parser/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY ./parser /parser

CMD ["python3", "parser.py"]