FROM python:3.6         
ADD . /todo
WORKDIR /todo
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]