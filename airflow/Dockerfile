FROM apache/airflow:2.3.0
COPY requirements.txt /
ENV BUCKET=${BUCKET}
ENV ORG=${ORG}
ENV TOKEN=${TOKEN}
ENV URL=${URL}
RUN pip install --no-cache-dir -r /requirements.txt