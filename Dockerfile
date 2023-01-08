FROM ubuntu:22.10
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]