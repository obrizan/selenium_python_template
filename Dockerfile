FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest", "tests", "--html=test-reports/report.html", "--self-contained-html", "-vvv"]
