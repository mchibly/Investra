FROM python:3.11-slim
WORKDIR /app
COPY fundamentus_scraper.py /app/
CMD ["python", "/app/fundamentus_scraper.py"]
