FROM python:3.10-slim

# Install system dependencies for libpostal
RUN apt-get update && \
    apt-get install -y git curl autoconf automake libtool pkg-config build-essential \
    libsnappy-dev ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install libpostal from source (compatible version)
RUN git clone https://github.com/openvenues/libpostal && \
    cd libpostal && \
    ./bootstrap.sh && \
    ./configure --datadir=/usr/local/share/libpostal && \
    make && make install && \
    ldconfig && \
    cd .. && rm -rf libpostal

# Set env var for postal
ENV LIBPOSTAL_DATA_DIR=/usr/local/share/libpostal

# Install Python dependencies (including postal)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your project files
COPY . /app
WORKDIR /app

# Default command (can be changed)
CMD ["bash"]