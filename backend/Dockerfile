FROM python
WORKDIR /app
COPY ./requirements.txt /app/
RUN  pip3 install -r ./requirements.txt
# Install Mosquitto clients
RUN apt-get update && apt-get install -y mosquitto-clients && rm -rf /var/lib/apt/lists/*
COPY . /app/
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]