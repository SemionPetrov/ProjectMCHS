FROM python:3.13.3-bookworm

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN apt-get -q update && apt-get -qy install netcat-traditional

EXPOSE 8000

CMD ["./wait-for", "-t", "30", "mysql:3306", "--", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

