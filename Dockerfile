FROM python:3.10.10-slim-buster
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    libcap-dev \
    libprotobuf-dev \
    protobuf-compiler \
    iproute2 \
    bison \
    flex \
    clang \
    cmake \
    pkg-config \
    libnl-3-dev \
    libnl-route-3-dev \
    curl

RUN mkdir /app

RUN git clone https://github.com/google/nsjail.git /opt/nsjail && \
    cd /opt/nsjail && \
    make && \
    cp nsjail /usr/local/bin/

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
# Run the application
EXPOSE 8080
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]