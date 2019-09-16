FROM python:3.6.5

# Create web directory
WORKDIR /var/app/www

# Install web dependencies
COPY Pipfile* ./

RUN apt-get update && \
    apt-get install build-essential software-properties-common libicu-dev python-pyicu -y;

# Install pipenv
RUN pip install pexpect uvicorn pipenv;

RUN pipenv install --system;

# Bundle web source
COPY . .