FROM python:3.13.3-bookworm

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN apt-get -q update && apt-get -qy install netcat-traditional

EXPOSE 8000

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

CMD ["entrypoint.sh"]
