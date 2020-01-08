FROM python:3.8-buster

# Install Inkscape
RUN apt-get update \
  && apt-get -y install inkscape unzip

# Install Node
RUN mkdir /node
WORKDIR /node
ENV NODE_VERSION 8.17.0
RUN ARCH= && dpkgArch="$(dpkg --print-architecture)" \
  && case "${dpkgArch##*-}" in \
    amd64) ARCH='x64';; \
    ppc64el) ARCH='ppc64le';; \
    s390x) ARCH='s390x';; \
    arm64) ARCH='arm64';; \
    armhf) ARCH='armv7l';; \
    i386) ARCH='x86';; \
    *) echo "unsupported architecture"; exit 1 ;; \
  esac \
  && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner

# Set up Cron
RUN apt-get -y install cron
COPY tasks /etc/cron.d/tasks
RUN chmod 0644 /etc/cron.d/tasks && crontab /etc/cron.d/tasks

# Copy the app files
COPY ./api /app
COPY ./frontend /frontend

# Build and install the frontend
WORKDIR /frontend
RUN npm install \
  && npm run build \
  && cp -rf /frontend/build /app

# Install the python app
WORKDIR /app
RUN pip install -r requirements.txt

# Cleanup
RUN rm -rf /usr/local/bin/node \
  && rm -rf /usr/local/bin/npm \
  && rm -rf /node \
  && rm -rf /frontend

WORKDIR /app
EXPOSE 8000
COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
