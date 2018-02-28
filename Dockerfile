FROM python:3.6         
ADD . /todo
WORKDIR /todo
EXPOSE 5000
RUN pip install --process-dependency-links -r requirements.txt
ENTRYPOINT ["python", "server.py"]