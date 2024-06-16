FROM python:3.10

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    && apt-get clean


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "app.main"]


