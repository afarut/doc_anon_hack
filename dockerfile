FROM python:3.8.10

COPY . .

RUN pip install -r req.txt

RUN pip freeze

RUN python -m spacy download ru_core_news_sm

CMD ["python", "-u", "main.py"]
