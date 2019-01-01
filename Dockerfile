FROM python:3.6.5

# Create web directory
WORKDIR /usr/src/app

# Install web dependencies
COPY Pipfile* ./

RUN apt-get -qq update && \
    apt-get -qq install build-essential software-properties-common libicu-dev python-pyicu -y;

# Install pipenv
RUN pip install pipenv;

RUN pipenv install --system && polyglot download LANG:pt;

# Bundle web source
COPY . .

EXPOSE 7010
CMD [ "python", "run.py" ]