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
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:3000", "server.app:app"]