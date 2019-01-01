curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
export PATH="/app/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv install 3.6.7

sudo apt-get install build-essential software-properties-common libicu-dev python-pyicu -y
pip install pipenv
pipenv install --system
find / -iname '*.cpp' -exec echo sed -i 's/locale\.h/locale2.h/g' '{}' ';'
