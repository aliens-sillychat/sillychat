FROM ubuntu:latest

# KoNLPy dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

# Install Java
RUN apt-get install -y openjdk-8-jdk
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

# install python
RUN apt-get install -y python3-pip python3-dev
RUN cd /usr/local/bin && \
  ln -s /usr/bin/python3 python && \
  ln -s /usr/bin/pip3 pip && \
  pip install --upgrade pip

WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "main.py"]
