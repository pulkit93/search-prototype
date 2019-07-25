# Use Python v3.7
FROM python:3.7

# Setup app working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY requirements/base.txt ./

# Install app dependencies
RUN pip install --no-cache-dir -r base.txt

# Copy sourcecode
COPY . .

# Start app
CMD ["gunicorn", "--config=python:gunicorn_config", "server.app:app"]